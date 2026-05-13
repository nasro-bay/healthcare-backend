
# 🚑 Healthcare Routing Engine (Algiers)
A modular Python navigation system that finds the shortest path to the nearest appropriate hospital in Algiers using OpenStreetMap data.

## ✨ Features
- **Algorithms**: A*, Dijkstra, BFS, DFS, and Hill Climbing.
- **Triage**: AI-powered symptom analysis using OpenAI (with local keyword fallback).
- **Graph Logic**: Virtual node injection and traffic-aware routing.
- **API**: Flask-based REST API for frontend integration.

## 🚀 Execution Guidelines
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the API Server**:
   ```bash
   python main.py
   ```
3. **Run Performance Benchmarks**:
   ```bash
   python evaluate_performance.py
   ```
4. **Run Tests**:
   ```bash
   python -m unittest discover tests
   ```
