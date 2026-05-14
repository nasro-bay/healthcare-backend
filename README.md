
#  Healthcare Routing Engine (Algiers)
A modular Python navigation system that finds the shortest path to the nearest appropriate hospital in Algiers using OpenStreetMap data.

##  Features
- **Algorithms**: A*, Dijkstra, BFS, DFS, and Hill Climbing.
- **Triage**: AI-powered symptom analysis using OpenAI (with local keyword fallback).
- **Graph Logic**: Virtual node injection and traffic-aware routing.
- **API**: Flask-based REST API for frontend integration.

##  Prerequisites
- Python 3.8+
- pip (Python package manager)

##  Local Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 (Optional): Set OpenAI API Key
For AI-powered symptom analysis (uses local keyword fallback if not set):
```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# Mac/Linux
export OPENAI_API_KEY=your_api_key_here
```

### Step 3: Start the Backend Server
```bash
python main.py
```
The API will be available at `http://localhost:5000` and accessible from other machines on the network.

##  Using the API

### Test the API
Open your browser and go to: `http://localhost:5000`

### API Endpoints
- `POST /api/users` - Submit symptoms and get hospital route
- `GET /route.html` - View the generated route map

##  Running Tests
```bash
python -m unittest discover tests
```

##  Performance Benchmarks
```bash
python evaluate_performance.py
```

##  Troubleshooting
- **API not accessible from another machine?** 
  - Check firewall: Port 5000 must be open
  - Verify backend is running: `python main.py`
  - Try accessing `http://<YOUR_IP>:5000` from another machine
