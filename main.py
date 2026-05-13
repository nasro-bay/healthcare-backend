
# Hospital-GUI/Hospital-GUI/server/main.py

import os
import sys
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from openai import OpenAI

# Add current directory to path for modular imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from healthcare.hospitals import SPECIALTY_MENU, get_hospital_availability
from healthcare.problem import HealthcareProblem
from config.settings import OUTPUT_PATH, DEFAULT_INITIAL_STATE
from graph.loader import load_graph
from graph.utils import cost
from visualization.map_renderer import render_route
import osmnx as ox

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("WARNING: OPENAI_API_KEY not found in environment variables.")
client = OpenAI(api_key=API_KEY)

# Global Graph Cache
print("Initializing Healthcare System...")
G, G_PROJ = load_graph()

@app.route('/')
def home():
    return "Healthcare Navigation API is Running. Use /api/users for navigation."

@app.route('/route.html')
def serve_route():
    return send_from_directory(os.path.dirname(OUTPUT_PATH), 'route.html')

def get_patient_specialty(symptoms):
    """
    Uses OpenAI to map symptoms to a medical specialty, with a local keyword fallback.
    """
    symptoms_lower = symptoms.lower()
    
    # Local Keyword Fallback Logic (Handles quota errors or offline mode)
    fallback_map = {
        "pediatric": "Pediatrics (طب الأطفال)",
        "child": "Pediatrics (طب الأطفال)",
        "baby": "Pediatrics (طب الأطفال)",
        "heart": "Cardiology (طب القلب)",
        "cardiac": "Cardiology (طب القلب)",
        "chest pain": "Cardiology (طب القلب)",
        "pregnant": "Obstetrics and Gynecology (طب التوليد والنساء والولادة)",
        "woman": "Obstetrics and Gynecology (طب التوليد والنساء والولادة)",
        "birth": "Obstetrics and Gynecology (طب التوليد والنساء والولادة)",
        "bone": "Orthopedics (طب العظام)",
        "fracture": "Orthopedics (طب العظام)",
        "break": "Orthopedics (طب العظام)",
        "eye": "Ophthalmology (طب العيون)",
        "skin": "Dermatology (طب الجلدية)",
        "rash": "Dermatology (طب الجلدية)",
        "stomach": "Gastroenterology (أمراض الجهاز الهضمي)",
        "surgery": "Surgery (General and Specialized) (الجراحة العامة والمتخصصة)",
        "emergency": "Emergency Medicine (طب الطوارئ)",
        "accident": "Emergency Medicine (طب الطوارئ)",
        "blood": "Emergency Medicine (طب الطوارئ)"
    }

    specialties_list = [v['name'] for v in SPECIALTY_MENU.values()]
    specialties_str = ", ".join(specialties_list)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        f"You are a medical triage assistant. Based on patient symptoms, "
                        f"identify the most suitable specialty from this list: {specialties_str}. "
                        f"Just return the exact specialty name from the list. If not found, say 'NOT FOUND'."
                    )
                },
                {"role": "user", "content": symptoms}
            ],
            timeout=5 # Avoid hanging
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}. Using keyword fallback...")
        
        # Search for keywords
        for keyword, specialty in fallback_map.items():
            if keyword in symptoms_lower:
                return specialty
                
        return "Emergency Medicine (طب الطوارئ)"

@app.route('/api/users', methods=['POST'])
def handle_navigation():
    """
    Main endpoint for patient navigation.
    """
    payload = request.json or {}
    symptoms = payload.get('data', '')
    lat = payload.get('lat')
    lon = payload.get('lon')
    strategy = payload.get('strategy', 'A_STAR')

    # Use defaults if coordinates are missing
    if lat is None or lon is None:
        lat, lon = DEFAULT_INITIAL_STATE
        print(f"Coordinates missing. Using default location: {lat}, {lon}")
    else:
        lat, lon = float(lat), float(lon)

    # 1. Identify Specialty
    specialty_name = get_patient_specialty(symptoms)
    print(f"Detected Specialty: {specialty_name}")

    # 2. Find Specialty Data
    target_osmids = []
    for entry in SPECIALTY_MENU.values():
        if entry['name'] == specialty_name:
            target_osmids = entry['osmids']
            break
    
    if not target_osmids:
        # Fallback to Emergency if not found
        target_osmids = SPECIALTY_MENU["5"]["osmids"]
        specialty_name = SPECIALTY_MENU["5"]["name"]

    try:
        # 3. Solve Problem
        problem = HealthcareProblem(
            initial_coords=(lat, lon),
            goal_osmids_list=target_osmids,
            G=G,
            G_projected=G_PROJ
        )
        
        route = problem.solve(strategy)
        
        if not route:
            return jsonify({"error": "No route found to any available hospital"}), 404

        # 4. Generate Metadata
        total_dist_m = cost(G, route)
        hospital_id = route[-1]
        
        # 5. Render Map
        render_route(G, route, OUTPUT_PATH)

        return jsonify({
            "result": [
                f"Hospital ID: {hospital_id}", 
                f"Specialty: {specialty_name}",
                f"Distance: {total_dist_m/1000:.2f} km",
                "Success"
            ],
            "project7": {
                "route_distance_km": round(total_dist_m/1000, 2),
                "hospital_id": hospital_id,
                "specialty": specialty_name
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/project7/meta', methods=['GET'])
def get_meta():
    return jsonify({
        "status": "active",
        "specialties": [v['name'] for v in SPECIALTY_MENU.values()]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
