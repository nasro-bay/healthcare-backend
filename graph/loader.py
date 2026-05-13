
# healthcare-navigation/graph/loader.py

import os
import osmnx
from config.settings import MAP_FILE, PLACE_NAME, NETWORK_TYPE

def load_graph():
    """
    Loads the road network graph of Algiers.
    Checks for a local cache file first; if missing, downloads from OSM.
    Returns:
        (G, G_projected): A tuple containing the base graph and the projected graph.
    """
    if os.path.exists(MAP_FILE):
        print(f"Loading map from local cache: {MAP_FILE}")
        G = osmnx.load_graphml(filepath=MAP_FILE)
    else:
        print(f"Local cache not found. Downloading map for '{PLACE_NAME}'...")
        # Ensure data directory exists
        os.makedirs(os.path.dirname(MAP_FILE), exist_ok=True)
        G = osmnx.graph_from_place(PLACE_NAME, network_type=NETWORK_TYPE)
        osmnx.save_graphml(G, filepath=MAP_FILE)
        print(f"Map saved to {MAP_FILE}")

    print("Projecting graph for faster coordinate lookups...")
    G_projected = osmnx.project_graph(G)
    return G, G_projected
