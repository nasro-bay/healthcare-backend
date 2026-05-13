
# healthcare-navigation/graph/utils.py

import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Computes the haversine distance between two points in meters.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371000  # Radius of Earth in meters
    return c * r

def cost(G, route):
    """
    Calculates the total distance of a route in meters.
    Args:
        G: The graph.
        route: A list of OSMID integers.
    Returns:
        float: Total distance in meters.
    """
    total_length = 0.0
    for u, v in zip(route, route[1:]):
        # We assume the first edge data is sufficient (MultiDiGraph)
        total_length += G[u][v][0]['length']
    return round(total_length, 4)
