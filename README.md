# Fuel Route Planner (Django 6.1 + DRF)

**Author:** Anant Sharma  
**Email:** anantsharma7091@gmail.com  
**Stack:** Python 3.14, Django 6.1, Django REST Framework, Leaflet.js, OSRM Routing, SciPy KD-Tree

Given a start and finish inside the USA, returns the driving route, the cost-optimal fuel stops (500-mile range), and total fuel spend at 10 MPG.

---

## 🚀 Quick Start (Running on Your System)

### Option 1: Double-Click Launcher
Simply double-click **`run_server.bat`** in this folder. It will launch the local development server and open the interactive map in your browser.

### Option 2: Command Line
```bash
# 1. Activate Virtual Environment
.\.venv\Scripts\activate

# 2. Run Database Migrations (already prepared)
python manage.py migrate

# 3. Import Fuel Stations (already pre-loaded: 6,626 US stations)
python manage.py import_stations

# 4. Run the Server
python manage.py runserver 127.0.0.1:8000
```
Open your browser at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Running Tests
To run the automated test suite:
```bash
.\.venv\Scripts\python.exe manage.py test
```
All 8 test cases verify routing feasibility, gas-station greedy optimization matching brute-force DP, station corridor snapping, and API response schema.

---

## 🌐 API Endpoints

### 1. Route Planning API
`POST /api/route/` (or `GET /api/route/?start=...&finish=...`)
```json
{
  "start": "Los Angeles, CA",
  "finish": "New York, NY",
  "range_miles": 500,
  "mpg": 10
}
```

#### Response Parameters:
- `distance_miles`: Total driving distance
- `duration_hours`: Estimated travel time
- `total_fuel_cost`: Minimum total fuel expenditure
- `total_gallons_purchased`: Total gallons purchased across all stops
- `fuel_stops[]`: List of optimal fuel stops (stop number, station name, city/state, price per gallon, gallons pumped, stop cost, route mile)
- `map`: GeoJSON FeatureCollection with the full route path and waypoint pins
- `map_url`: Link to the interactive visual map
- `author`: "Anant Sharma"

### 2. Interactive Map UI
`GET /` or `GET /api/route/map/?start=...&finish=...`
Interactive Leaflet web interface allowing direct search, quick presets (LA → NYC, Miami → Seattle, etc.), visual waypoint pins, and real-time fuel calculation metrics.

---

## ⚡ Architecture & Optimization Highlights

| Concern | Approach |
|---|---|
| **External calls** | **One** OSRM call per route (`overview=full`, GeoJSON). Route is cached for 24h, so parameter tweaks or repeat runs make **zero** external calls. |
| **Geocoding** | `lat,lng` parsed locally; `City, ST` resolved via offline gazetteer (`zipcodes`). Nominatim is only a fallback for free-form addresses. |
| **Station coordinates** | Geocoded offline once by city/state (6,626/6,626 US stations matched) and stored in SQLite. |
| **Route Corridor Filter** | In-memory station array + SciPy `cKDTree` snaps all ~6.6k stations to route vertices within milliseconds. |
| **Optimal Stop Strategy** | Greedy gas-station algorithm: purchase just enough fuel to reach a cheaper station ahead within vehicle range; otherwise fill the tank and advance to the cheapest reachable station. |
