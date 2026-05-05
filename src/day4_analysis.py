# TripVerse - Day 4 - Advanced Data Analysis
import sqlite3
import pandas as pd

# Database connect karo
def connect_db():
    conn = sqlite3.connect("database/tripverse.db")
    return conn

conn = connect_db()
conn = sqlite3.connect("database/tripverse.db")
print("=" * 50)
print("  TRIPVERSE - DAY 4 - DATA ANALYSIS")
print("=" * 50)

# 1. Destinations analysis
print("\n All Destinations:")
df = pd.read_sql("SELECT * FROM destinations", conn)
print(df.to_string(index=False))

# 2. State wise destinations count
print("\n State wise Destinations:")
df2 = pd.read_sql("""
    SELECT state, COUNT(*) as total_destinations,
    AVG(avg_budget) as average_budget
    FROM destinations
    GROUP BY state
    ORDER BY average_budget DESC
""", conn)
print(df2.to_string(index=False))

# 3. Category wise analysis
print("\n📈 Category wise Budget:")
df3 = pd.read_sql("""
    SELECT category,
    COUNT(*) as total,
    MIN(avg_budget) as min_budget,
    MAX(avg_budget) as max_budget,
    AVG(avg_budget) as avg_budget
    FROM destinations
    GROUP BY category
    ORDER BY avg_budget DESC
""", conn)
print(df3.to_string(index=False))

# 4. Top vendors by rating
print("\n Top Vendors:")
df4 = pd.read_sql("""
    SELECT name, vendor_type, location,
    price, rating
    FROM vendors
    ORDER BY rating DESC
""", conn)
print(df4.to_string(index=False))

# 5. Vendor type wise average price
print("\n Vendor Type wise Avg Price:")
df5 = pd.read_sql("""
    SELECT vendor_type,
    COUNT(*) as total_vendors,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
    FROM vendors
    GROUP BY vendor_type
    ORDER BY avg_price DESC
""", conn)
print(df5.to_string(index=False))

# 6. Budget friendly destinations for students
print("\n Student Budget Destinations (Under Rs.10000):")
df6 = pd.read_sql("""
    SELECT name, state, category, avg_budget
    FROM destinations
    WHERE avg_budget <= 10000
    ORDER BY avg_budget ASC
""", conn)
print(df6.to_string(index=False))

# 7. Luxury destinations
print("\n Luxury Destinations (Above Rs.15000):")
df7 = pd.read_sql("""
    SELECT name, state, category, avg_budget
    FROM destinations
    WHERE avg_budget >= 15000
    ORDER BY avg_budget DESC
""", conn)
print(df7.to_string(index=False))

conn.close()
print("\n Day 4 Analysis Complete!")