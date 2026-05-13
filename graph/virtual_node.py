
# healthcare-navigation/graph/virtual_node.py

import osmnx
from shapely import Point
from graph.utils import haversine_distance
from config.settings import VIRTUAL_NODE_THRESHOLD

def get_nearest_node(coords, G, G_projected):
    """
    Finds the nearest node to the given coordinates.
    If the coordinates are very close to an edge, a virtual node is injected.
    Args:
        coords: (lat, lon) tuple.
        G: Base graph.
        G_projected: Projected graph for faster lookup.
    Returns:
        int: The OSMID of the nearest (possibly virtual) node.
    """
    lat, lon = coords
    
    # Project the point to match the graph's CRS
    point_geom = Point(lon, lat)
    point_geom_proj, _ = osmnx.projection.project_geometry(point_geom, to_crs=G_projected.graph['crs'])
    x, y = point_geom_proj.x, point_geom_proj.y

    # Find the nearest edge and distance to it in meters
    (u, v, k), dist = osmnx.nearest_edges(G_projected, x, y, return_dist=True)

    if dist < VIRTUAL_NODE_THRESHOLD:
        # User is extremely close to a road: inject a virtual node
        virtual_id = max(G.nodes()) + 1
        G.add_node(virtual_id, x=lon, y=lat)
        
        # Calculate distances from virtual node to edge endpoints
        d_u = haversine_distance(lat, lon, G.nodes[u]['y'], G.nodes[u]['x'])
        d_v = haversine_distance(lat, lon, G.nodes[v]['y'], G.nodes[v]['x'])
        
        # Connect virtual node to the network
        G.add_edge(virtual_id, u, length=d_u)
        G.add_edge(virtual_id, v, length=d_v)
        return virtual_id
    else:
        # Too far from an edge: snap to the nearest existing intersection
        return osmnx.nearest_nodes(G, lon, lat)
