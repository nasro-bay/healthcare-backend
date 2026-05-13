
# healthcare-navigation/config/settings.py

import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File Paths
MAP_FILE = os.path.join(BASE_DIR, "data", "algiers_drive.graphml")
HOSPITALS_FILE = os.path.join(BASE_DIR, "data", "hospitals.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "route.html")

# OpenStreetMap Configuration
PLACE_NAME = "Algiers, Algeria"
NETWORK_TYPE = "drive"

# Algorithm Constants
VIRTUAL_NODE_THRESHOLD = 5  # meters
EARTH_RADIUS_KM = 6371

# Default user location (School location)
DEFAULT_INITIAL_STATE = (36.688626588752726, 2.866251759424538)
