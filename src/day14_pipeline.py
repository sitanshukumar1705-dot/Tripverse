# TripVerse - Day 14 - Complete Data Pipeline
import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  🔄 TRIPVERSE - DAY 14 - DATA PIPELINE")
print("=" * 55)

conn = sqlite3.connect("database/tripverse.db")

# =====================================
# STEP 1 - DATABASE HEALTH CHECK
# =====================================
print("\n🏥 Step 1: Database Health Check...")

tables = [
    'users', 'vendors', 'destinations',
    'bookings', 'reviews', 'rewards',
    'budget_plans', 'admin',
    'sentiment_reviews', 'user_segments',
    'booking_trends', 'price_trends',
    'destination_coordinates', 'distance_matrix',
    'weather_data'
]

print("\n" + "=" * 55)
print("  DATABASE HEALTH REPORT")
print("=" * 55)

total_records = 0
healthy_tables = 0

for table in tables:
    try:
        df = pd.read_sql(
            f"SELECT COUNT(*) as count FROM {table}",
            conn
        )
        count = df['count'][0]
        total_records += count
        status = "✅ Healthy" if count > 0 else "⚠️  Empty"
        if count > 0:
            healthy_tables += 1
        print(f"  {status} {table:<25} → {count:>5} records")
    except Exception as e:
        print(f"  ❌ Error  {table:<25} → {str(e)[:20]}")

print(f"\n  Total Tables   : {len(tables)}")
print(f"  Healthy Tables : {healthy_tables}")
print(f"  Total Records  : {total_records:,}")

# =====================================
# STEP 2 - DATA QUALITY CHECK
# =====================================
print("\n\n🔍 Step 2: Data Quality Check...")

print("\n" + "=" * 55)
print("  DATA QUALITY REPORT")
print("=" * 55)

# Users quality check
users_df = pd.read_sql("SELECT * FROM users", conn)
print(f"\n  👥 Users Table:")
print(f"     Total Users    : {len(users_df)}")
print(f"     Missing Names  : {users_df['name'].isnull().sum()}")
print(f"     Missing Emails : {users_df['email'].isnull().sum()}")
print(f"     User Types     : {users_df['user_type'].unique().tolist()}")

# Vendors quality check
vendors_df = pd.read_sql("SELECT * FROM vendors", conn)
print(f"\n  🏢 Vendors Table:")
print(f"     Total Vendors    : {len(vendors_df)}")
print(f"     Verified         : {vendors_df['is_verified'].sum()}")
print(f"     Active           : {vendors_df['is_active'].sum()}")
print(f"     Avg Rating       : {vendors_df['rating'].mean():.2f}")
print(f"     Vendor Types     : {vendors_df['vendor_type'].unique().tolist()}")

# Destinations quality check
dest_df = pd.read_sql("SELECT * FROM destinations", conn)
print(f"\n  🌍 Destinations Table:")
print(f"     Total Destinations : {len(dest_df)}")
print(f"     Categories         : {dest_df['category'].unique().tolist()}")
print(f"     Budget Range       : Rs.{dest_df['avg_budget'].min():,} - Rs.{dest_df['avg_budget'].max():,}")
print(f"     Avg Budget         : Rs.{dest_df['avg_budget'].mean():,.0f}")

# =====================================
# STEP 3 - MASTER ANALYTICS
# =====================================
print("\n\n" + "=" * 55)
print("  📊 MASTER ANALYTICS DASHBOARD")
print("=" * 55)

# Revenue Analysis
print("\n  💰 Revenue Insights:")
booking_trends = pd.read_sql(
    "SELECT * FROM booking_trends", conn
)
price_trends = pd.read_sql(
    "SELECT * FROM price_trends", conn
)

dest_cols = ['Jaipur', 'Goa', 'Manali', 'Kerala', 'Ladakh']
total_revenue = 0
for dest in dest_cols:
    if dest in booking_trends.columns and \
       dest in price_trends.columns:
        rev = (booking_trends[dest] *
               price_trends[dest]).sum()
        total_revenue += rev
        print(f"     {dest:<12}: Rs.{rev:>15,.0f}")

print(f"\n     {'Total':<12}: Rs.{total_revenue:>15,.0f}")

# Weather Insights
print("\n  🌤️  Weather Insights:")
weather_df = pd.read_sql(
    "SELECT * FROM weather_data", conn
)
best_weather = weather_df.loc[
    weather_df['weather_score'].idxmax()
]
worst_weather = weather_df.loc[
    weather_df['weather_score'].idxmin()
]
print(f"     Best Weather  : {best_weather['destination']}"
      f" in {best_weather['month']}"
      f" (Score: {best_weather['weather_score']:.0f})")
print(f"     Worst Weather : {worst_weather['destination']}"
      f" in {worst_weather['month']}"
      f" (Score: {worst_weather['weather_score']:.0f})")

# Sentiment Insights
print("\n  ⭐ Sentiment Insights:")
sentiment_df = pd.read_sql(
    "SELECT * FROM sentiment_reviews", conn
)
positive = len(sentiment_df[
    sentiment_df['sentiment'].str.contains('Positive')
])
negative = len(sentiment_df[
    sentiment_df['sentiment'].str.contains('Negative')
])
print(f"     Total Reviews  : {len(sentiment_df)}")
print(f"     Positive       : {positive} ({positive/len(sentiment_df)*100:.1f}%)")
print(f"     Negative       : {negative} ({negative/len(sentiment_df)*100:.1f}%)")
print(f"     Avg Rating     : {sentiment_df['rating'].mean():.2f}/5")

# User Segments
print("\n  👥 User Segments:")
segments_df = pd.read_sql(
    "SELECT * FROM user_segments", conn
)
segment_dist = segments_df['cluster'].value_counts()
segment_names = {
    0: "Budget", 1: "Family",
    2: "Luxury", 3: "Adventure",
    4: "Beach",  5: "Heritage"
}
for cluster, count in segment_dist.items():
    name = segment_names.get(cluster, f"Seg {cluster}")
    print(f"     {name:<12}: {count} users")

# =====================================
# STEP 4 - COMPLETE TRIP ADVISOR
# =====================================
print("\n\n" + "=" * 55)
print("  🧳 COMPLETE TRIP ADVISOR")
print("=" * 55)

def complete_trip_advisor(user_type, budget,
                           travel_month, days):
    print(f"\n  User     : {user_type}")
    print(f"  Budget   : Rs.{budget:,}")
    print(f"  Month    : {travel_month}")
    print(f"  Days     : {days}")
    print(f"  {'─'*45}")

    # Weather data
    weather_df_local = pd.read_sql(
        f"SELECT * FROM weather_data "
        f"WHERE month='{travel_month}'",
        conn
    )

    # Destination data
    dest_df_local = pd.read_sql(
        "SELECT * FROM destinations", conn
    )

    recommendations = []

    for _, dest in dest_df_local.iterrows():
        dest_name = dest['name']

        # Budget score
        budget_score = 1 - abs(
            dest['avg_budget'] - budget
        ) / budget
        budget_score = max(0, budget_score)

        # Weather score
        weather_row = weather_df_local[
            weather_df_local['destination'] == dest_name
        ]
        if len(weather_row) > 0:
            weather_score = weather_row[
                'weather_score'
            ].values[0] / 150
        else:
            weather_score = 0.5

        # Final score
        final_score = (budget_score * 0.5 +
                      weather_score * 0.5)

        recommendations.append({
            'destination': dest_name,
            'state':       dest['state'],
            'category':    dest['category'],
            'avg_budget':  dest['avg_budget'],
            'budget_score': round(budget_score, 2),
            'weather_score': round(weather_score, 2),
            'final_score':   round(final_score, 2)
        })

    recommendations.sort(
        key=lambda x: x['final_score'],
        reverse=True
    )

    print(f"\n  🏆 Top Recommendations:")
    print(f"  {'Destination':<12}"
          f"{'Category':<12}"
          f"{'Budget':>8}"
          f"{'B.Score':>8}"
          f"{'W.Score':>8}"
          f"{'Final':>7}")
    print(f"  {'─'*60}")

    for rec in recommendations[:5]:
        print(f"  {rec['destination']:<12}"
              f"{rec['category']:<12}"
              f"Rs.{rec['avg_budget']:>5,}"
              f"{rec['budget_score']:>8.2f}"
              f"{rec['weather_score']:>8.2f}"
              f"{rec['final_score']:>7.2f}")

# Test Complete Advisor
complete_trip_advisor("Student", 8000, "Nov", 5)
complete_trip_advisor("Luxury", 100000, "Jun", 10)

# =====================================
# STEP 5 - DATA PIPELINE SUMMARY
# =====================================
print("\n\n" + "=" * 55)
print("  🔄 DATA PIPELINE SUMMARY")
print("=" * 55)

pipeline_stages = [
    ("Day 1-2",  "Foundation",
     "Python basics + Multilingual system"),
    ("Day 3-4",  "Database",
     "SQL setup + Advanced analysis"),
    ("Day 5",    "Visualization",
     "5 charts with Matplotlib"),
    ("Day 6",    "ML Model",
     "Price prediction (Linear Regression)"),
    ("Day 7",    "Database V2",
     "8 tables + JSON migration"),
    ("Day 8",    "Recommendation",
     "Content + Collaborative filtering"),
    ("Day 9",    "NLP",
     "Sentiment analysis + Fake detection"),
    ("Day 10",   "Clustering",
     "K-Means user segmentation"),
    ("Day 11",   "Time Series",
     "Demand forecasting + Seasonal analysis"),
    ("Day 12",   "Location",
     "Maps + Route optimizer"),
    ("Day 13",   "Weather",
     "Weather scoring + API simulation"),
    ("Day 14",   "Pipeline",
     "Complete integration ✅"),
]

for days, phase, description in pipeline_stages:
    print(f"  ✅ {days:<10} {phase:<15} → {description}")

# =====================================
# STEP 6 - FINAL VISUALIZATION
# =====================================
print("\n📊 Step 6: Generating Pipeline Charts...")

if not os.path.exists("charts"):
    os.makedirs("charts")

# Chart 1 - Complete Dashboard
fig = plt.figure(figsize=(16, 12))
fig.suptitle('TripVerse - Master Analytics Dashboard',
             fontsize=16, fontweight='bold', y=0.98)

# Plot 1 - Revenue by Destination
ax1 = fig.add_subplot(2, 3, 1)
revenues = []
for dest in dest_cols:
    if dest in booking_trends.columns:
        rev = (booking_trends[dest] *
               price_trends[dest]).sum()
        revenues.append(rev / 1000000)

bars = ax1.bar(dest_cols, revenues,
               color=['#3498db', '#e74c3c', '#2ecc71',
                      '#f39c12', '#9b59b6'])
ax1.set_title('Revenue (Millions Rs.)',
              fontweight='bold')
ax1.set_xticklabels(dest_cols, rotation=45,
                    fontsize=8)

# Plot 2 - Sentiment Distribution
ax2 = fig.add_subplot(2, 3, 2)
sent_counts = sentiment_df['sentiment'].apply(
    lambda x: x.split()[0]
).value_counts()
ax2.pie(sent_counts.values,
        labels=sent_counts.index,
        autopct='%1.1f%%',
        colors=['#2ecc71', '#e74c3c', '#95a5a6'])
ax2.set_title('Review Sentiment',
              fontweight='bold')

# Plot 3 - User Segments
ax3 = fig.add_subplot(2, 3, 3)
seg_labels = [segment_names.get(i, f'Seg {i}')
              for i in segment_dist.index]
ax3.bar(seg_labels, segment_dist.values,
        color=['#3498db', '#2ecc71', '#e74c3c',
               '#f39c12', '#9b59b6', '#1abc9c'])
ax3.set_title('User Segments',
              fontweight='bold')
ax3.set_xticklabels(seg_labels, rotation=45,
                    fontsize=8)

# Plot 4 - Weather Scores
ax4 = fig.add_subplot(2, 3, 4)
weather_pivot = weather_df.pivot(
    index='destination',
    columns='month',
    values='weather_score'
)
month_order = ['Jan', 'Feb', 'Mar', 'Apr',
               'May', 'Jun', 'Jul', 'Aug',
               'Sep', 'Oct', 'Nov', 'Dec']
weather_pivot = weather_pivot[
    [m for m in month_order
     if m in weather_pivot.columns]
]
im = ax4.imshow(weather_pivot.values,
                cmap='RdYlGn', aspect='auto')
ax4.set_xticks(range(len(weather_pivot.columns)))
ax4.set_xticklabels(weather_pivot.columns,
                    fontsize=7, rotation=45)
ax4.set_yticks(range(len(weather_pivot.index)))
ax4.set_yticklabels(weather_pivot.index, fontsize=8)
ax4.set_title('Weather Score Heatmap',
              fontweight='bold')

# Plot 5 - Destination Budget
ax5 = fig.add_subplot(2, 3, 5)
ax5.barh(dest_df['name'],
         dest_df['avg_budget'],
         color='#3498db')
ax5.set_title('Destination Budgets (Rs.)',
              fontweight='bold')
ax5.set_xlabel('Average Budget')

# Plot 6 - Vendor Ratings
ax6 = fig.add_subplot(2, 3, 6)
ax6.bar(vendors_df['name'],
        vendors_df['rating'],
        color=['#2ecc71' if r >= 4.5
               else '#f39c12' if r >= 4.0
               else '#e74c3c'
               for r in vendors_df['rating']])
ax6.set_title('Vendor Ratings',
              fontweight='bold')
ax6.set_xticklabels(vendors_df['name'],
                    rotation=45, fontsize=7)
ax6.set_ylim(3.5, 5.2)

plt.tight_layout()
plt.savefig('charts/21_master_dashboard.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("✅ Master Dashboard chart saved!")

conn.close()

print("\n" + "=" * 55)
print("  🎉 DAY 14 COMPLETE!")
print("=" * 55)
print("\n  ✅ Database Health Check Done!")
print("  ✅ Data Quality Report Done!")
print("  ✅ Master Analytics Ready!")
print("  ✅ Complete Trip Advisor!")
print("  ✅ Pipeline Summary Done!")
print("  ✅ Master Dashboard Chart!")
print("\n  🏆 DATA SCIENCE PHASE COMPLETE!")
print("  📅 Next: Web Development Phase!")
print("      Day 15-21: Flask + HTML + CSS")