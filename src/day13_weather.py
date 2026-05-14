# TripVerse - Day 13 - Weather Analysis & API Integration
import sqlite3
import pandas as pd
import numpy as np
import requests
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  🌤️  TRIPVERSE - DAY 13 - WEATHER ANALYSIS")
print("=" * 55)

# =====================================
# DATABASE CONNECT
# =====================================
conn = sqlite3.connect("database/tripverse.db")

# =====================================
# STEP 1 - WEATHER DATA (SIMULATED)
# =====================================
print("\n🌡️  Step 1: Loading Weather Dataset...")

# Realistic weather data for Indian destinations
weather_data = {
    'Jaipur': {
        'Jan': {'temp_max': 22, 'temp_min': 8,  'humidity': 55, 'rainfall': 5,  'condition': 'Sunny'},
        'Feb': {'temp_max': 25, 'temp_min': 11, 'humidity': 48, 'rainfall': 5,  'condition': 'Sunny'},
        'Mar': {'temp_max': 31, 'temp_min': 16, 'humidity': 40, 'rainfall': 5,  'condition': 'Hot'},
        'Apr': {'temp_max': 37, 'temp_min': 22, 'humidity': 30, 'rainfall': 5,  'condition': 'Very Hot'},
        'May': {'temp_max': 41, 'temp_min': 26, 'humidity': 28, 'rainfall': 10, 'condition': 'Very Hot'},
        'Jun': {'temp_max': 39, 'temp_min': 26, 'humidity': 45, 'rainfall': 20, 'condition': 'Hot'},
        'Jul': {'temp_max': 34, 'temp_min': 25, 'humidity': 70, 'rainfall': 80, 'condition': 'Monsoon'},
        'Aug': {'temp_max': 32, 'temp_min': 24, 'humidity': 75, 'rainfall': 70, 'condition': 'Monsoon'},
        'Sep': {'temp_max': 33, 'temp_min': 23, 'humidity': 65, 'rainfall': 30, 'condition': 'Cloudy'},
        'Oct': {'temp_max': 33, 'temp_min': 18, 'humidity': 45, 'rainfall': 10, 'condition': 'Pleasant'},
        'Nov': {'temp_max': 27, 'temp_min': 12, 'humidity': 50, 'rainfall': 5,  'condition': 'Pleasant'},
        'Dec': {'temp_max': 22, 'temp_min': 7,  'humidity': 55, 'rainfall': 5,  'condition': 'Cool'},
    },
    'Goa': {
        'Jan': {'temp_max': 32, 'temp_min': 19, 'humidity': 65, 'rainfall': 5,  'condition': 'Perfect'},
        'Feb': {'temp_max': 33, 'temp_min': 20, 'humidity': 62, 'rainfall': 2,  'condition': 'Perfect'},
        'Mar': {'temp_max': 34, 'temp_min': 23, 'humidity': 68, 'rainfall': 5,  'condition': 'Warm'},
        'Apr': {'temp_max': 35, 'temp_min': 25, 'humidity': 72, 'rainfall': 10, 'condition': 'Warm'},
        'May': {'temp_max': 33, 'temp_min': 26, 'humidity': 78, 'rainfall': 50, 'condition': 'Pre-Monsoon'},
        'Jun': {'temp_max': 30, 'temp_min': 24, 'humidity': 88, 'rainfall': 500,'condition': 'Heavy Monsoon'},
        'Jul': {'temp_max': 29, 'temp_min': 24, 'humidity': 90, 'rainfall': 600,'condition': 'Heavy Monsoon'},
        'Aug': {'temp_max': 29, 'temp_min': 24, 'humidity': 89, 'rainfall': 450,'condition': 'Heavy Monsoon'},
        'Sep': {'temp_max': 30, 'temp_min': 23, 'humidity': 82, 'rainfall': 200,'condition': 'Monsoon'},
        'Oct': {'temp_max': 32, 'temp_min': 22, 'humidity': 70, 'rainfall': 40, 'condition': 'Pleasant'},
        'Nov': {'temp_max': 33, 'temp_min': 20, 'humidity': 63, 'rainfall': 10, 'condition': 'Perfect'},
        'Dec': {'temp_max': 32, 'temp_min': 19, 'humidity': 62, 'rainfall': 5,  'condition': 'Perfect'},
    },
    'Manali': {
        'Jan': {'temp_max': -1, 'temp_min': -10,'humidity': 75, 'rainfall': 80, 'condition': 'Heavy Snow'},
        'Feb': {'temp_max': 1,  'temp_min': -8, 'humidity': 72, 'rainfall': 70, 'condition': 'Snow'},
        'Mar': {'temp_max': 8,  'temp_min': -2, 'humidity': 65, 'rainfall': 50, 'condition': 'Snow/Cold'},
        'Apr': {'temp_max': 14, 'temp_min': 4,  'humidity': 58, 'rainfall': 30, 'condition': 'Cold'},
        'May': {'temp_max': 19, 'temp_min': 8,  'humidity': 52, 'rainfall': 40, 'condition': 'Pleasant'},
        'Jun': {'temp_max': 23, 'temp_min': 12, 'humidity': 55, 'rainfall': 50, 'condition': 'Best Season'},
        'Jul': {'temp_max': 21, 'temp_min': 13, 'humidity': 75, 'rainfall': 90, 'condition': 'Monsoon'},
        'Aug': {'temp_max': 20, 'temp_min': 12, 'humidity': 78, 'rainfall': 80, 'condition': 'Monsoon'},
        'Sep': {'temp_max': 18, 'temp_min': 8,  'humidity': 65, 'rainfall': 40, 'condition': 'Pleasant'},
        'Oct': {'temp_max': 11, 'temp_min': 2,  'humidity': 58, 'rainfall': 20, 'condition': 'Cold'},
        'Nov': {'temp_max': 4,  'temp_min': -4, 'humidity': 68, 'rainfall': 40, 'condition': 'Very Cold'},
        'Dec': {'temp_max': -1, 'temp_min': -10,'humidity': 72, 'rainfall': 60, 'condition': 'Heavy Snow'},
    },
    'Kerala': {
        'Jan': {'temp_max': 31, 'temp_min': 20, 'humidity': 72, 'rainfall': 20, 'condition': 'Pleasant'},
        'Feb': {'temp_max': 32, 'temp_min': 21, 'humidity': 70, 'rainfall': 15, 'condition': 'Pleasant'},
        'Mar': {'temp_max': 33, 'temp_min': 23, 'humidity': 73, 'rainfall': 30, 'condition': 'Warm'},
        'Apr': {'temp_max': 33, 'temp_min': 24, 'humidity': 78, 'rainfall': 80, 'condition': 'Pre-Monsoon'},
        'May': {'temp_max': 32, 'temp_min': 24, 'humidity': 82, 'rainfall': 150,'condition': 'Pre-Monsoon'},
        'Jun': {'temp_max': 29, 'temp_min': 23, 'humidity': 88, 'rainfall': 450,'condition': 'Heavy Monsoon'},
        'Jul': {'temp_max': 28, 'temp_min': 22, 'humidity': 90, 'rainfall': 500,'condition': 'Heavy Monsoon'},
        'Aug': {'temp_max': 28, 'temp_min': 22, 'humidity': 89, 'rainfall': 420,'condition': 'Heavy Monsoon'},
        'Sep': {'temp_max': 29, 'temp_min': 22, 'humidity': 85, 'rainfall': 250,'condition': 'Monsoon'},
        'Oct': {'temp_max': 30, 'temp_min': 22, 'humidity': 82, 'rainfall': 250,'condition': 'Monsoon'},
        'Nov': {'temp_max': 30, 'temp_min': 21, 'humidity': 78, 'rainfall': 100,'condition': 'Post-Monsoon'},
        'Dec': {'temp_max': 30, 'temp_min': 20, 'humidity': 74, 'rainfall': 30, 'condition': 'Pleasant'},
    },
    'Leh Ladakh': {
        'Jan': {'temp_max': -3, 'temp_min': -14,'humidity': 40, 'rainfall': 10, 'condition': 'Extreme Cold'},
        'Feb': {'temp_max': -1, 'temp_min': -12,'humidity': 38, 'rainfall': 10, 'condition': 'Extreme Cold'},
        'Mar': {'temp_max': 5,  'temp_min': -7, 'humidity': 35, 'rainfall': 10, 'condition': 'Very Cold'},
        'Apr': {'temp_max': 12, 'temp_min': 0,  'humidity': 30, 'rainfall': 5,  'condition': 'Cold'},
        'May': {'temp_max': 18, 'temp_min': 5,  'humidity': 28, 'rainfall': 5,  'condition': 'Pleasant'},
        'Jun': {'temp_max': 24, 'temp_min': 10, 'humidity': 25, 'rainfall': 5,  'condition': 'Best Season'},
        'Jul': {'temp_max': 27, 'temp_min': 14, 'humidity': 30, 'rainfall': 15, 'condition': 'Best Season'},
        'Aug': {'temp_max': 26, 'temp_min': 13, 'humidity': 32, 'rainfall': 15, 'condition': 'Best Season'},
        'Sep': {'temp_max': 21, 'temp_min': 7,  'humidity': 28, 'rainfall': 5,  'condition': 'Pleasant'},
        'Oct': {'temp_max': 12, 'temp_min': -2, 'humidity': 30, 'rainfall': 5,  'condition': 'Cold'},
        'Nov': {'temp_max': 2,  'temp_min': -10,'humidity': 35, 'rainfall': 5,  'condition': 'Very Cold'},
        'Dec': {'temp_max': -3, 'temp_min': -14,'humidity': 38, 'rainfall': 10, 'condition': 'Extreme Cold'},
    }
}

print(f"✅ Weather data loaded for {len(weather_data)} destinations!")

# =====================================
# STEP 2 - BEST TIME TO VISIT
# =====================================
print("\n📅 Step 2: Best Time to Visit Analysis...")

def get_weather_score(weather):
    score = 100

    # Temperature scoring
    temp_avg = (weather['temp_max'] + weather['temp_min']) / 2
    if 15 <= temp_avg <= 28:
        score += 30   # Perfect temperature
    elif 10 <= temp_avg <= 32:
        score += 15   # Good temperature
    elif temp_avg < 0:
        score -= 30   # Too cold
    elif temp_avg > 35:
        score -= 20   # Too hot

    # Rainfall scoring
    if weather['rainfall'] < 20:
        score += 20   # Dry weather
    elif weather['rainfall'] < 100:
        score += 5    # Light rain
    elif weather['rainfall'] > 300:
        score -= 40   # Heavy rain

    # Humidity scoring
    if weather['humidity'] < 60:
        score += 10   # Comfortable
    elif weather['humidity'] > 85:
        score -= 15   # Too humid

    return score

print("\n" + "=" * 55)
print("  🌟 BEST TIME TO VISIT")
print("=" * 55)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for dest, monthly_weather in weather_data.items():
    scores = []
    for month in months:
        score = get_weather_score(monthly_weather[month])
        scores.append(score)

    best_month  = months[np.argmax(scores)]
    worst_month = months[np.argmin(scores)]
    best_score  = max(scores)
    worst_score = min(scores)

    print(f"\n  📍 {dest}")
    print(f"     Best Month  : {best_month}"
          f" (Score: {best_score})")
    print(f"     Avoid Month : {worst_month}"
          f" (Score: {worst_score})")
    print(f"     Best Condition: "
          f"{monthly_weather[best_month]['condition']}")

# =====================================
# STEP 3 - WEATHER BASED TRIP ADVISOR
# =====================================
print("\n\n" + "=" * 55)
print("  🧳 WEATHER BASED TRIP ADVISOR")
print("=" * 55)

def weather_trip_advisor(travel_month, user_type):
    print(f"\n  Month: {travel_month} | User: {user_type}")
    print(f"  {'─'*45}")

    recommendations = []
    for dest, monthly_weather in weather_data.items():
        weather = monthly_weather[travel_month]
        score = get_weather_score(weather)

        # User type preferences
        if user_type == "Adventure" and \
           weather['condition'] in ['Best Season', 'Pleasant']:
            score += 20
        elif user_type == "Beach" and \
             weather['condition'] in ['Perfect', 'Sunny']:
            score += 20
        elif user_type == "Family" and \
             weather['rainfall'] < 50:
            score += 15

        recommendations.append({
            'destination': dest,
            'condition':   weather['condition'],
            'temp_max':    weather['temp_max'],
            'temp_min':    weather['temp_min'],
            'rainfall':    weather['rainfall'],
            'score':       score
        })

    recommendations.sort(
        key=lambda x: x['score'], reverse=True
    )

    print(f"  {'Destination':<15}"
          f"{'Condition':<18}"
          f"{'Temp':>6}"
          f"{'Rain':>8}"
          f"{'Score':>7}")
    print(f"  {'─'*55}")

    for rec in recommendations[:4]:
        print(f"  {rec['destination']:<15}"
              f"{rec['condition']:<18}"
              f"{rec['temp_min']}°-{rec['temp_max']}°C"
              f"{rec['rainfall']:>5}mm"
              f"{rec['score']:>7}")

# Test different scenarios
weather_trip_advisor("Jun", "Adventure")
weather_trip_advisor("Dec", "Beach")
weather_trip_advisor("Oct", "Family")

# =====================================
# STEP 4 - WEATHER ALERTS
# =====================================
print("\n\n" + "=" * 55)
print("  🚨 WEATHER ALERTS SYSTEM")
print("=" * 55)

def generate_weather_alerts(destination, month):
    weather = weather_data[destination][month]
    alerts = []

    if weather['rainfall'] > 300:
        alerts.append({
            'type': '🔴 HIGH ALERT',
            'message': f"Heavy rainfall expected "
                      f"({weather['rainfall']}mm). "
                      f"Avoid outdoor activities!"
        })

    if weather['temp_max'] > 40:
        alerts.append({
            'type': '🟠 HEAT ALERT',
            'message': f"Extreme heat ({weather['temp_max']}°C). "
                      f"Carry water, avoid noon travel!"
        })

    if weather['temp_min'] < -5:
        alerts.append({
            'type': '🔵 COLD ALERT',
            'message': f"Extreme cold ({weather['temp_min']}°C). "
                      f"Carry heavy woollens!"
        })

    if weather['humidity'] > 85:
        alerts.append({
            'type': '🟡 HUMIDITY ALERT',
            'message': f"High humidity ({weather['humidity']}%). "
                      f"Stay hydrated!"
        })

    if not alerts:
        alerts.append({
            'type': '🟢 ALL CLEAR',
            'message': f"Weather is {weather['condition']}. "
                      f"Perfect time to visit!"
        })

    return alerts

# Test alerts
test_cases = [
    ('Goa', 'Jul'),
    ('Jaipur', 'May'),
    ('Leh Ladakh', 'Jan'),
    ('Kerala', 'Dec'),
    ('Manali', 'Jun'),
]

for dest, month in test_cases:
    weather = weather_data[dest][month]
    alerts = generate_weather_alerts(dest, month)
    print(f"\n  📍 {dest} - {month}:")
    print(f"     Temp: {weather['temp_min']}°C to "
          f"{weather['temp_max']}°C | "
          f"Rain: {weather['rainfall']}mm")
    for alert in alerts:
        print(f"     {alert['type']}: {alert['message']}")

# =====================================
# STEP 5 - MONTHLY WEATHER COMPARISON
# =====================================
print("\n\n" + "=" * 55)
print("  📊 MONTHLY WEATHER SUMMARY")
print("=" * 55)

for dest in list(weather_data.keys())[:3]:
    print(f"\n  📍 {dest}:")
    print(f"  {'Month':<6}"
          f"{'Max°C':>7}"
          f"{'Min°C':>7}"
          f"{'Rain':>7}"
          f"{'Condition':<20}"
          f"{'Rating':>8}")
    print(f"  {'─'*60}")

    for month in months:
        w = weather_data[dest][month]
        score = get_weather_score(w)
        if score >= 130:
            rating = "⭐⭐⭐⭐⭐"
        elif score >= 115:
            rating = "⭐⭐⭐⭐"
        elif score >= 100:
            rating = "⭐⭐⭐"
        elif score >= 85:
            rating = "⭐⭐"
        else:
            rating = "⭐"

        print(f"  {month:<6}"
              f"{w['temp_max']:>7}"
              f"{w['temp_min']:>7}"
              f"{w['rainfall']:>7}"
              f"{w['condition']:<20}"
              f"  {rating}")

# =====================================
# STEP 6 - API SIMULATION
# =====================================
print("\n\n" + "=" * 55)
print("  🌐 WEATHER API SIMULATION")
print("=" * 55)

def simulate_weather_api(city, month):
    if city in weather_data and month in weather_data[city]:
        weather = weather_data[city][month]
        api_response = {
            "status": "success",
            "city": city,
            "month": month,
            "data": {
                "temperature": {
                    "max": weather['temp_max'],
                    "min": weather['temp_min'],
                    "unit": "celsius"
                },
                "humidity": weather['humidity'],
                "rainfall": {
                    "amount": weather['rainfall'],
                    "unit": "mm"
                },
                "condition": weather['condition'],
                "travel_advisory": generate_weather_alerts(
                    city, month
                )[0]['message'],
                "weather_score": get_weather_score(weather),
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
        }
    else:
        api_response = {
            "status": "error",
            "message": "City or month not found"
        }

    return api_response

print("\n  Simulated API Response:")
response = simulate_weather_api("Goa", "Dec")
print(f"\n  {json.dumps(response, indent=4)}")

# =====================================
# STEP 7 - VISUALIZATION
# =====================================
print("\n📊 Step 7: Generating Weather Charts...")

if not os.path.exists("charts"):
    os.makedirs("charts")

# Chart 1 - Temperature Trends
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

colors = ['#e74c3c', '#3498db', '#2ecc71',
          '#f39c12', '#9b59b6']

for i, (dest, monthly_w) in enumerate(
    weather_data.items()
):
    temps_max = [monthly_w[m]['temp_max'] for m in months]
    axes[0].plot(months, temps_max,
                 label=dest, color=colors[i],
                 linewidth=2, marker='o')

axes[0].set_title(
    'TripVerse - Monthly Max Temperature by Destination',
    fontsize=13, fontweight='bold'
)
axes[0].set_ylabel('Max Temperature (°C)', fontsize=11)
axes[0].legend(loc='upper right')
axes[0].axhline(y=35, color='red',
                linestyle='--', alpha=0.5,
                label='Too Hot (35°C)')
axes[0].grid(True, alpha=0.3)

# Chart 2 - Rainfall
for i, (dest, monthly_w) in enumerate(
    weather_data.items()
):
    rainfall = [monthly_w[m]['rainfall'] for m in months]
    axes[1].plot(months, rainfall,
                 label=dest, color=colors[i],
                 linewidth=2, marker='s')

axes[1].set_title(
    'TripVerse - Monthly Rainfall by Destination',
    fontsize=13, fontweight='bold'
)
axes[1].set_ylabel('Rainfall (mm)', fontsize=11)
axes[1].set_xlabel('Month', fontsize=11)
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('charts/19_weather_trends.png', dpi=150)
plt.close()

# Chart 2 - Weather Score Heatmap
weather_scores = np.zeros(
    (len(weather_data), 12)
)
dest_names = list(weather_data.keys())

for i, dest in enumerate(dest_names):
    for j, month in enumerate(months):
        weather_scores[i, j] = get_weather_score(
            weather_data[dest][month]
        )

fig, ax = plt.subplots(figsize=(14, 6))
im = ax.imshow(weather_scores,
               cmap='RdYlGn', aspect='auto',
               vmin=50, vmax=150)
ax.set_xticks(range(12))
ax.set_xticklabels(months)
ax.set_yticks(range(len(dest_names)))
ax.set_yticklabels(dest_names)
plt.colorbar(im, label='Weather Score')
ax.set_title(
    'TripVerse - Weather Score Heatmap\n'
    '(Green=Best, Red=Worst)',
    fontsize=14, fontweight='bold'
)

for i in range(len(dest_names)):
    for j in range(12):
        ax.text(j, i,
                f'{weather_scores[i,j]:.0f}',
                ha='center', va='center',
                fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/20_weather_heatmap.png', dpi=150)
plt.close()

print("✅ 2 Weather Charts saved!")

# =====================================
# STEP 8 - DATABASE SAVE
# =====================================
print("\n💾 Step 8: Saving Weather Data to Database...")

weather_records = []
for dest, monthly_w in weather_data.items():
    for month, w in monthly_w.items():
        weather_records.append({
            'destination': dest,
            'month': month,
            'temp_max': w['temp_max'],
            'temp_min': w['temp_min'],
            'humidity': w['humidity'],
            'rainfall': w['rainfall'],
            'condition': w['condition'],
            'weather_score': get_weather_score(w)
        })

weather_df = pd.DataFrame(weather_records)
weather_df.to_sql(
    'weather_data',
    conn,
    if_exists='replace',
    index=False
)

print(f"✅ {len(weather_records)} weather records saved!")
conn.close()

print("\n" + "=" * 55)
print("  🎉 DAY 13 COMPLETE!")
print("=" * 55)
print("\n  ✅ Weather Data for 5 Destinations!")
print("  ✅ Best Time to Visit Analysis!")
print("  ✅ Weather Based Trip Advisor!")
print("  ✅ Smart Weather Alerts!")
print("  ✅ API Response Simulation!")
print("  ✅ 2 Charts Generated!")
print("  ✅ Weather Data Saved to Database!")