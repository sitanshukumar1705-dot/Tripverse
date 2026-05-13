# TripVerse - Day 12 - Location & Geospatial Features
import sqlite3
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import folium
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  🗺️  TRIPVERSE - DAY 12 - LOCATION FEATURES")
print("=" * 55)

# =====================================
# DATABASE CONNECT
# =====================================
conn = sqlite3.connect("database/tripverse.db")

# =====================================
# STEP 1 - DESTINATION COORDINATES
# =====================================
print("\n📍 Step 1: Setting Up Destination Coordinates...")

destinations = {
    'Jaipur':     {'lat': 26.9124, 'lon': 75.7873,
                   'state': 'Rajasthan',
                   'category': 'Heritage',
                   'avg_budget': 8000},
    'Goa':        {'lat': 15.2993, 'lon': 74.1240,
                   'state': 'Goa',
                   'category': 'Beach',
                   'avg_budget': 12000},
    'Manali':     {'lat': 32.2396, 'lon': 77.1887,
                   'state': 'Himachal Pradesh',
                   'category': 'Adventure',
                   'avg_budget': 10000},
    'Kerala':     {'lat': 10.8505, 'lon': 76.2711,
                   'state': 'Kerala',
                   'category': 'Nature',
                   'avg_budget': 15000},
    'Varanasi':   {'lat': 25.3176, 'lon': 82.9739,
                   'state': 'UP',
                   'category': 'Spiritual',
                   'avg_budget': 6000},
    'Leh Ladakh': {'lat': 34.1526, 'lon': 77.5771,
                   'state': 'J&K',
                   'category': 'Adventure',
                   'avg_budget': 25000},
    'Mumbai':     {'lat': 19.0760, 'lon': 72.8777,
                   'state': 'Maharashtra',
                   'category': 'City',
                   'avg_budget': 10000},
    'Darjeeling': {'lat': 27.0360, 'lon': 88.2627,
                   'state': 'West Bengal',
                   'category': 'Hills',
                   'avg_budget': 9000},
    'Agra':       {'lat': 27.1767, 'lon': 78.0081,
                   'state': 'UP',
                   'category': 'Heritage',
                   'avg_budget': 7000},
    'Andaman':    {'lat': 11.7401, 'lon': 92.6586,
                   'state': 'Andaman',
                   'category': 'Beach',
                   'avg_budget': 20000},
    'Delhi':      {'lat': 28.6139, 'lon': 77.2090,
               'state': 'Delhi',
               'category': 'City',
               'avg_budget': 8000},
}

print(f"✅ {len(destinations)} destinations loaded!")

# =====================================
# STEP 2 - DISTANCE CALCULATOR
# =====================================
print("\n📏 Step 2: Distance Calculator...")

def calculate_distance(city1, city2):
    loc1 = (destinations[city1]['lat'],
             destinations[city1]['lon'])
    loc2 = (destinations[city2]['lat'],
             destinations[city2]['lon'])
    distance = geodesic(loc1, loc2).kilometers
    return round(distance, 1)

print("\n  Distance Matrix (km):")
cities = list(destinations.keys())[:6]
print(f"\n  {'From/To':<15}", end='')
for city in cities:
    print(f"{city[:8]:>10}", end='')
print()
print("  " + "─" * 75)

for city1 in cities:
    print(f"  {city1:<15}", end='')
    for city2 in cities:
        if city1 == city2:
            print(f"{'0':>10}", end='')
        else:
            dist = calculate_distance(city1, city2)
            print(f"{dist:>10}", end='')
    print()

# =====================================
# STEP 3 - NEARBY DESTINATIONS
# =====================================
print("\n\n🔍 Step 3: Nearby Destinations Finder...")

def find_nearby(user_city, max_distance=500):
    if user_city not in destinations:
        return []

    nearby = []
    for dest, info in destinations.items():
        if dest != user_city:
            dist = calculate_distance(user_city, dest)
            if dist <= max_distance:
                nearby.append({
                    'destination': dest,
                    'distance_km': dist,
                    'category': info['category'],
                    'avg_budget': info['avg_budget'],
                    'state': info['state']
                })

    nearby.sort(key=lambda x: x['distance_km'])
    return nearby

# Test nearby finder
test_cities = ['Jaipur', 'Mumbai', 'Manali']
for city in test_cities:
    print(f"\n  📍 Nearby {city} (within 500km):")
    nearby = find_nearby(city, 500)
    if nearby:
        for place in nearby:
            print(f"     → {place['destination']:<15}"
                  f" {place['distance_km']:>6} km"
                  f" | {place['category']:<12}"
                  f" | Rs.{place['avg_budget']:,}")
    else:
        print("     No destinations within 500km!")

# =====================================
# STEP 4 - ROUTE OPTIMIZER
# =====================================
print("\n\n🛣️  Step 4: Route Optimizer...")

def optimize_route(start_city, dest_list):
    if not dest_list:
        return []

    route = [start_city]
    remaining = dest_list.copy()
    current = start_city
    total_dist = 0

    while remaining:
        min_dist = float('inf')
        next_city = None

        for city in remaining:
            dist = calculate_distance(current, city)
            if dist < min_dist:
                min_dist = dist
                next_city = city

        route.append(next_city)
        total_dist += min_dist
        current = next_city
        remaining.remove(next_city)

    return route, total_dist

# Test route optimizer
print("\n  🗺️  Golden Triangle + Extensions:")
route_cities = ['Agra', 'Jaipur', 'Varanasi']
optimized_route, total_km = optimize_route(
    'Delhi', route_cities
)

print(f"\n  Start: Delhi")
print(f"  Destinations: {route_cities}")
print(f"\n  Optimized Route:")
prev = 'Delhi'
total = 0

for i, city in enumerate(optimized_route):
    if city != 'Delhi':
        dist = calculate_distance(prev, city) if prev in destinations else 0
        total += dist
        print(f"  {i}. {prev} → {city}: {dist:.0f} km")
        prev = city

print(f"\n  Total Distance: {total:.0f} km")
print(f"  Route: {' → '.join(['Delhi'] + optimized_route)}")

# =====================================
# STEP 5 - LOCATION BASED RECOMMENDATION
# =====================================
print("\n\n🎯 Step 5: Location Based Recommendations...")

def location_recommend(user_lat, user_lon,
                        user_budget, max_dist=1000):
    recommendations = []

    for dest, info in destinations.items():
        dest_loc = (info['lat'], info['lon'])
        user_loc = (user_lat, user_lon)
        dist = geodesic(user_loc, dest_loc).kilometers

        if dist <= max_dist:
            budget_match = 1 - abs(
                info['avg_budget'] - user_budget
            ) / user_budget
            budget_match = max(0, budget_match)

            score = (budget_match * 0.6 +
                    (1 - dist/max_dist) * 0.4)

            recommendations.append({
                'destination': dest,
                'distance_km': round(dist, 0),
                'avg_budget': info['avg_budget'],
                'category': info['category'],
                'score': round(score, 2)
            })

    recommendations.sort(
        key=lambda x: x['score'], reverse=True
    )
    return recommendations[:5]

# Test from different cities
test_locations = [
    (28.6139, 77.2090, 8000, "Delhi"),
    (19.0760, 72.8777, 15000, "Mumbai"),
    (12.9716, 77.5946, 10000, "Bangalore"),
]

for lat, lon, budget, city in test_locations:
    print(f"\n  📍 User in {city}"
          f" (Budget: Rs.{budget:,}):")
    recs = location_recommend(lat, lon, budget)
    print(f"  {'Destination':<15}"
          f"{'Distance':>10}"
          f"{'Budget':>10}"
          f"{'Score':>8}")
    print(f"  {'─'*45}")
    for rec in recs:
        print(f"  {rec['destination']:<15}"
              f"{rec['distance_km']:>8} km"
              f" Rs.{rec['avg_budget']:>6,}"
              f"{rec['score']:>8}")

# =====================================
# STEP 6 - INDIA MAP BANAO
# =====================================
print("\n\n🗺️  Step 6: Creating Interactive India Map...")

india_map = folium.Map(
    location=[20.5937, 78.9629],
    zoom_start=5,
    tiles='OpenStreetMap'
)

category_colors = {
    'Heritage':  'red',
    'Beach':     'blue',
    'Adventure': 'green',
    'Nature':    'darkgreen',
    'Spiritual': 'orange',
    'Hills':     'purple',
    'City':      'gray'
}

for dest, info in destinations.items():
    color = category_colors.get(
        info['category'], 'blue'
    )

    popup_html = f"""
    <div style='width:200px'>
        <h4>{dest}</h4>
        <b>State:</b> {info['state']}<br>
        <b>Category:</b> {info['category']}<br>
        <b>Avg Budget:</b> Rs.{info['avg_budget']:,}<br>
    </div>
    """

    folium.Marker(
        location=[info['lat'], info['lon']],
        popup=folium.Popup(popup_html,
                          max_width=250),
        tooltip=f"{dest} - Rs.{info['avg_budget']:,}",
        icon=folium.Icon(color=color,
                         icon='info-sign')
    ).add_to(india_map)

folium.LayerControl().add_to(india_map)

if not os.path.exists("maps"):
    os.makedirs("maps")

india_map.save("maps/tripverse_india.html")
print("✅ Interactive map saved: maps/tripverse_india.html")

# =====================================
# STEP 7 - COORDINATES DATABASE
# =====================================
print("\n💾 Step 7: Saving to Database...")

dest_df = pd.DataFrame([
    {
        'name': dest,
        'latitude': info['lat'],
        'longitude': info['lon'],
        'state': info['state'],
        'category': info['category'],
        'avg_budget': info['avg_budget']
    }
    for dest, info in destinations.items()
])

dest_df.to_sql(
    'destination_coordinates',
    conn,
    if_exists='replace',
    index=False
)

print("✅ Coordinates saved to database!")

# =====================================
# STEP 8 - DISTANCE MATRIX DATABASE
# =====================================
print("\n💾 Step 8: Saving Distance Matrix...")

distance_records = []
for city1 in destinations:
    for city2 in destinations:
        if city1 != city2:
            dist = calculate_distance(city1, city2)
            distance_records.append({
                'from_city': city1,
                'to_city': city2,
                'distance_km': dist
            })

dist_df = pd.DataFrame(distance_records)
dist_df.to_sql(
    'distance_matrix',
    conn,
    if_exists='replace',
    index=False
)

print(f"✅ {len(distance_records)} distance"
      f" records saved!")

conn.close()

print("\n" + "=" * 55)
print("  🎉 DAY 12 COMPLETE!")
print("=" * 55)
print("\n  ✅ 10 Destination Coordinates Loaded!")
print("  ✅ Distance Matrix Calculated!")
print("  ✅ Nearby Destinations Finder Ready!")
print("  ✅ Route Optimizer Ready!")
print("  ✅ Location Based Recommendations!")
print("  ✅ Interactive India Map Created!")
print("  ✅ Data Saved to Database!")