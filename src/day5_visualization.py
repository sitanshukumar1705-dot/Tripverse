# TripVerse - Day 5 - Data Visualization
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Save as file
import matplotlib.pyplot as plt
import os

# =====================================
# DATABASE CONNECT
# =====================================
conn = sqlite3.connect("database/tripverse.db")

# Charts folder banao
if not os.path.exists("charts"):
    os.makedirs("charts")

print("=" * 50)
print("  📊 TRIPVERSE - DAY 5 - VISUALIZATION")
print("=" * 50)

# =====================================
# CHART 1 - DESTINATION BUDGET BAR CHART
# =====================================
df1 = pd.read_sql("""
    SELECT name, avg_budget
    FROM destinations
    ORDER BY avg_budget ASC
""", conn)

plt.figure(figsize=(12, 6))
colors = ['#2ecc71' if x <= 10000 else '#e74c3c' if x >= 15000
          else '#f39c12' for x in df1['avg_budget']]
bars = plt.bar(df1['name'], df1['avg_budget'], color=colors)
plt.title('TripVerse - Destination Budget Comparison', fontsize=16, fontweight='bold')
plt.xlabel('Destination', fontsize=12)
plt.ylabel('Average Budget (Rs.)', fontsize=12)
plt.xticks(rotation=45, ha='right')
for bar, val in zip(bars, df1['avg_budget']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
             f'Rs.{val:,}', ha='center', va='bottom', fontsize=9)
plt.legend(handles=[
    plt.Rectangle((0,0),1,1, color='#2ecc71', label='Student Budget'),
    plt.Rectangle((0,0),1,1, color='#f39c12', label='Family Budget'),
    plt.Rectangle((0,0),1,1, color='#e74c3c', label='Luxury Budget')
])
plt.tight_layout()
plt.savefig('charts/01_destination_budget.png', dpi=150)
plt.close()
print("\n✅ Chart 1 saved - Destination Budget!")

# =====================================
# CHART 2 - CATEGORY PIE CHART
# =====================================
df2 = pd.read_sql("""
    SELECT category, COUNT(*) as count
    FROM destinations
    GROUP BY category
""", conn)

plt.figure(figsize=(8, 8))
colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']
plt.pie(df2['count'], labels=df2['category'],
        autopct='%1.1f%%', colors=colors,
        startangle=90, shadow=True)
plt.title('TripVerse - Destination Categories', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/02_category_pie.png', dpi=150)
plt.close()
print("✅ Chart 2 saved - Category Distribution!")

# =====================================
# CHART 3 - VENDOR RATING BAR CHART
# =====================================
df3 = pd.read_sql("""
    SELECT name, vendor_type, rating
    FROM vendors
    ORDER BY rating DESC
""", conn)

plt.figure(figsize=(12, 6))
colors = ['#gold' if r >= 4.8 else '#silver' if r >= 4.5
          else '#cd7f32' for r in df3['rating']]
colors = ['#f1c40f' if r >= 4.8 else '#95a5a6' if r >= 4.5
          else '#e67e22' for r in df3['rating']]
bars = plt.bar(df3['name'], df3['rating'], color=colors)
plt.title('TripVerse - Vendor Ratings', fontsize=16, fontweight='bold')
plt.xlabel('Vendor', fontsize=12)
plt.ylabel('Rating (out of 5)', fontsize=12)
plt.ylim(3.5, 5.2)
plt.xticks(rotation=45, ha='right')
for bar, val in zip(bars, df3['rating']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{val}⭐', ha='center', va='bottom', fontsize=10)
plt.axhline(y=4.5, color='red', linestyle='--', alpha=0.7, label='Excellent (4.5+)')
plt.legend()
plt.tight_layout()
plt.savefig('charts/03_vendor_ratings.png', dpi=150)
plt.close()
print("✅ Chart 3 saved - Vendor Ratings!")

# =====================================
# CHART 4 - VENDOR TYPE PRICE COMPARISON
# =====================================
df4 = pd.read_sql("""
    SELECT vendor_type, AVG(price) as avg_price
    FROM vendors
    GROUP BY vendor_type
    ORDER BY avg_price DESC
""", conn)

plt.figure(figsize=(10, 6))
bars = plt.barh(df4['vendor_type'], df4['avg_price'],
                color=['#3498db', '#e74c3c', '#2ecc71',
                       '#f39c12', '#9b59b6', '#1abc9c', '#e67e22'])
plt.title('TripVerse - Average Price by Vendor Type', fontsize=16, fontweight='bold')
plt.xlabel('Average Price (Rs.)', fontsize=12)
plt.ylabel('Vendor Type', fontsize=12)
for bar, val in zip(bars, df4['avg_price']):
    plt.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
             f'Rs.{val:,.0f}', ha='left', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('charts/04_vendor_prices.png', dpi=150)
plt.close()
print("✅ Chart 4 saved - Vendor Prices!")

# =====================================
# CHART 5 - BUDGET CATEGORY COMPARISON
# =====================================
df5 = pd.read_sql("""
    SELECT category,
    AVG(avg_budget) as avg_cost,
    MIN(avg_budget) as min_cost,
    MAX(avg_budget) as max_cost
    FROM destinations
    GROUP BY category
    ORDER BY avg_cost
""", conn)

x = range(len(df5['category']))
width = 0.25

plt.figure(figsize=(12, 7))
plt.bar([i - width for i in x], df5['min_cost'],
        width, label='Min Budget', color='#2ecc71')
plt.bar(x, df5['avg_cost'],
        width, label='Avg Budget', color='#3498db')
plt.bar([i + width for i in x], df5['max_cost'],
        width, label='Max Budget', color='#e74c3c')
plt.title('TripVerse - Budget Range by Category',
          fontsize=16, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Budget (Rs.)', fontsize=12)
plt.xticks(x, df5['category'], rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('charts/05_budget_range.png', dpi=150)
plt.close()
print("✅ Chart 5 saved - Budget Range!")

conn.close()

print("\n" + "=" * 50)
print("  🎉 ALL 5 CHARTS SAVED IN 'charts' FOLDER!")
print("=" * 50)
print("\n📊 Charts Created:")
print("  1. Destination Budget Comparison")
print("  2. Category Distribution (Pie)")
print("  3. Vendor Ratings")
print("  4. Vendor Price Comparison")
print("  5. Budget Range by Category")
print("\n Day 5 Complete!")