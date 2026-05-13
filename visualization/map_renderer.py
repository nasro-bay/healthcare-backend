
# healthcare-navigation/visualization/map_renderer.py

import folium
import os
from graph.utils import cost

def render_route(G, route, output_path):
    """
    Renders the calculated route onto a Folium map and saves it.
    Args:
        G: Graph.
        route: List of OSMIDs.
        output_path: Path to save the HTML file.
    Returns:
        folium.Map: The map object.
    """
    if not route:
        print("\n[WARNING] No route found. Map rendering skipped.")
        return None
    
    total_meters = cost(G, route)
    print(f"\nSuccess! Path found.")
    print(f"Total distance: {total_meters / 1000:.2f} km")

    # Center map on start node
    start_node = G.nodes[route[0]]
    route_map = folium.Map(location=(start_node['y'], start_node['x']), zoom_start=14)
    
    # Get coordinates for the route
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    
    # Draw path
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(route_map)

    # Add markers
    folium.Marker(
        location=route_coords[0],
        popup='Start Location',
        icon=folium.Icon(color='green')
    ).add_to(route_map)
    
    folium.Marker(
        location=route_coords[-1],
        popup='Nearest Hospital',
        icon=folium.Icon(color='red')
    ).add_to(route_map)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    route_map.save(output_path)
    print(f"Map saved to: {output_path}")
    
    return route_map
