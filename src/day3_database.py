# TripVerse - Day 3 - SQL Database
import sqlite3
import pandas as pd
from datetime import datetime

# =====================================
# DATABASE CONNECTION
# =====================================

def connect_db():
    conn = sqlite3.connect("tripverse.db")
    return conn

# =====================================
# TABLES BANAO
# =====================================

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # 1. USERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            user_type   TEXT NOT NULL,
            budget      INTEGER,
            days        INTEGER,
            created_at  TEXT
        )
    ''')

    # 2. VENDORS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            vendor_type   TEXT NOT NULL,
            location      TEXT,
            price         INTEGER,
            rating        REAL,
            created_at    TEXT
        )
    ''')

    # 3. DESTINATIONS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS destinations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            state       TEXT NOT NULL,
            category    TEXT,
            best_season TEXT,
            avg_budget  INTEGER
        )
    ''')

    # 4. BOOKINGS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            vendor_id   INTEGER,
            destination TEXT,
            amount      INTEGER,
            status      TEXT,
            booked_at   TEXT,
            FOREIGN KEY (user_id)   REFERENCES users(id),
            FOREIGN KEY (vendor_id) REFERENCES vendors(id)
        )
    ''')

    conn.commit()
    conn.close()
    print(" All tables created successfully!")

# =====================================
# SAMPLE DATA DAALO
# =====================================

def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Destinations
    destinations = [
        ("Jaipur",      "Rajasthan",    "Heritage",   "October-March",  8000),
        ("Goa",         "Goa",          "Beach",      "November-March", 12000),
        ("Manali",      "Himachal",     "Adventure",  "March-June",     10000),
        ("Kerala",      "Kerala",       "Nature",     "September-March",15000),
        ("Varanasi",    "UP",           "Spiritual",  "October-March",  6000),
        ("Leh Ladakh",  "J&K",          "Adventure",  "June-September", 25000),
        ("Mumbai",      "Maharashtra",  "City",       "November-March", 10000),
        ("Darjeeling",  "West Bengal",  "Hills",      "March-May",      9000),
        ("Agra",        "UP",           "Heritage",   "October-March",  7000),
        ("Andaman",     "Andaman",      "Beach",      "October-May",    20000),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO destinations
        (name, state, category, best_season, avg_budget)
        VALUES (?, ?, ?, ?, ?)
    ''', destinations)

    # Sample Vendors
    vendors = [
        ("Hotel Taj",       "hotel",      "Jaipur",  5000,  4.5),
        ("GoAir Flights",   "flight",     "Mumbai",  3000,  4.0),
        ("Volvo Travels",   "bus",        "Manali",  800,   4.2),
        ("Spice Kitchen",   "restaurant", "Goa",     500,   4.7),
        ("Trek Adventures", "adventure",  "Ladakh",  2000,  4.8),
        ("Beach Resort",    "hotel",      "Goa",     8000,  4.6),
        ("Kerala Homestay", "homestay",   "Kerala",  2500,  4.9),
        ("Cab Express",     "cab",        "Agra",    600,   4.1),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO vendors
        (name, vendor_type, location, price, rating)
        VALUES (?, ?, ?, ?, ?)
    ''', vendors)

    conn.commit()
    conn.close()
    print(" Sample data inserted!")

# =====================================
# DATA DEKHNA - PANDAS SE
# =====================================

def view_data():
    conn = connect_db()

    print("\n" + "=" * 50)
    print("  🌍 TRIPVERSE - TOP DESTINATIONS")
    print("=" * 50)
    df = pd.read_sql("SELECT * FROM destinations", conn)
    print(df.to_string(index=False))

    print("\n" + "=" * 50)
    print("  🏢 TRIPVERSE - VENDORS")
    print("=" * 50)
    df2 = pd.read_sql("SELECT * FROM vendors", conn)
    print(df2.to_string(index=False))

    conn.close()

# =====================================
# SQL QUERIES - ANALYSIS
# =====================================

def analyze_data():
    conn = connect_db()

    print("\n" + "=" * 50)
    print("  📊 BUDGET ANALYSIS")
    print("=" * 50)

    # Sabse sasta destination
    df = pd.read_sql('''
        SELECT name, state, avg_budget
        FROM destinations
        ORDER BY avg_budget ASC
        LIMIT 3
    ''', conn)
    print("\n  💰 Top 3 Budget-Friendly Destinations:")
    print(df.to_string(index=False))

    # Category wise average budget
    df2 = pd.read_sql('''
        SELECT category, AVG(avg_budget) as avg_cost
        FROM destinations
        GROUP BY category
        ORDER BY avg_cost ASC
    ''', conn)
    print("\n  📈 Category wise Average Cost:")
    print(df2.to_string(index=False))

    # Top rated vendors
    df3 = pd.read_sql('''
        SELECT name, vendor_type, location, rating
        FROM vendors
        ORDER BY rating DESC
        LIMIT 5
    ''', conn)
    print("\n  ⭐ Top 5 Rated Vendors:")
    print(df3.to_string(index=False))

    conn.close()

# =====================================
# MAIN PROGRAM
# =====================================

print("=" * 50)
print("  🗄️  TRIPVERSE - DAY 3 - SQL DATABASE")
print("=" * 50)

# Tables banao
create_tables()

# Data daalo
insert_sample_data()

# Data dekho
view_data()

# Analysis karo
analyze_data()

print("\n✅ Day 3 Complete! Database ready!")