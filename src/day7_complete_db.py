# TripVerse - Day 7 - Complete Database Setup
import sqlite3
import json
import pandas as pd
from datetime import datetime

print("=" * 55)
print("  🗄️  TRIPVERSE - DAY 7 - COMPLETE DATABASE SETUP")
print("=" * 55)

# =====================================
# DATABASE CONNECTION
# =====================================

def connect_db():
    conn = sqlite3.connect("database/tripverse.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# =====================================
# STEP 1 - ALL TABLES BANAO
# =====================================

def create_all_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # 1. USERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            phone       TEXT,
            user_type   TEXT NOT NULL,
            language    TEXT DEFAULT 'English',
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
            owner_name    TEXT,
            owner_email   TEXT,
            location      TEXT,
            state         TEXT,
            price         INTEGER,
            rating        REAL DEFAULT 0.0,
            is_verified   INTEGER DEFAULT 0,
            is_active     INTEGER DEFAULT 1,
            created_at    TEXT
        )
    ''')

    # 3. DESTINATIONS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS destinations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL UNIQUE,
            state       TEXT NOT NULL,
            category    TEXT,
            best_season TEXT,
            avg_budget  INTEGER,
            description TEXT,
            is_active   INTEGER DEFAULT 1
        )
    ''')

    # 4. BOOKINGS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL,
            vendor_id       INTEGER NOT NULL,
            destination     TEXT,
            check_in        TEXT,
            check_out       TEXT,
            num_people      INTEGER DEFAULT 1,
            total_amount    INTEGER,
            status          TEXT DEFAULT 'Pending',
            token           TEXT UNIQUE,
            otp             TEXT,
            created_at      TEXT,
            FOREIGN KEY (user_id)   REFERENCES users(id),
            FOREIGN KEY (vendor_id) REFERENCES vendors(id)
        )
    ''')

    # 5. REVIEWS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            vendor_id   INTEGER NOT NULL,
            booking_id  INTEGER NOT NULL,
            rating      REAL NOT NULL,
            comment     TEXT,
            created_at  TEXT,
            FOREIGN KEY (user_id)   REFERENCES users(id),
            FOREIGN KEY (vendor_id) REFERENCES vendors(id),
            FOREIGN KEY (booking_id) REFERENCES bookings(id)
        )
    ''')

    # 6. REWARDS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rewards (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            points      INTEGER DEFAULT 0,
            type        TEXT,
            description TEXT,
            created_at  TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 7. ADMIN TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            username    TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            created_at  TEXT
        )
    ''')

    # 8. BUDGET PLANS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget_plans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type   TEXT UNIQUE NOT NULL,
            min_budget  INTEGER NOT NULL,
            max_budget  INTEGER NOT NULL,
            updated_at  TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("\n✅ All 8 Tables Created Successfully!")
    print("   users, vendors, destinations, bookings,")
    print("   reviews, rewards, admin, budget_plans")

# =====================================
# STEP 2 - SAMPLE DATA INSERT
# =====================================

def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Destinations
    destinations = [
        ("Jaipur",     "Rajasthan",   "Heritage",  "October-March",   8000,  "Pink City of India"),
        ("Goa",        "Goa",         "Beach",     "November-March",  12000, "Party capital of India"),
        ("Manali",     "Himachal",    "Adventure", "March-June",      10000, "Gateway to Himalayan adventures"),
        ("Kerala",     "Kerala",      "Nature",    "September-March", 15000, "Gods own country"),
        ("Varanasi",   "UP",          "Spiritual", "October-March",   6000,  "Spiritual capital of India"),
        ("Leh Ladakh", "J&K",         "Adventure", "June-September",  25000, "Land of high passes"),
        ("Mumbai",     "Maharashtra", "City",      "November-March",  10000, "City of dreams"),
        ("Darjeeling", "West Bengal", "Hills",     "March-May",       9000,  "Queen of hills"),
        ("Agra",       "UP",          "Heritage",  "October-March",   7000,  "City of Taj Mahal"),
        ("Andaman",    "Andaman",     "Beach",     "October-May",     20000, "Emerald islands of India"),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO destinations
        (name, state, category, best_season, avg_budget, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', destinations)

    # Vendors
    vendors = [
        ("Hotel Taj",        "hotel",      "Raj Sharma",   "raj@taj.com",     "Jaipur",  "Rajasthan", 5000, 4.5, 1, 1, now),
        ("GoAir Flights",    "flight",     "Air Team",     "air@goair.com",   "Mumbai",  "Maharashtra",3000, 4.0, 1, 1, now),
        ("Volvo Travels",    "bus",        "Ram Singh",    "ram@volvo.com",   "Manali",  "Himachal",  800,  4.2, 1, 1, now),
        ("Spice Kitchen",    "restaurant", "Chef Mohan",   "chef@spice.com",  "Goa",     "Goa",       500,  4.7, 1, 1, now),
        ("Trek Adventures",  "adventure",  "Arjun Nair",   "arjun@trek.com",  "Ladakh",  "J&K",       2000, 4.8, 1, 1, now),
        ("Beach Resort",     "hotel",      "Priya Menon",  "priya@beach.com", "Goa",     "Goa",       8000, 4.6, 1, 1, now),
        ("Kerala Homestay",  "homestay",   "Thomas K",     "thomas@kh.com",   "Kerala",  "Kerala",    2500, 4.9, 1, 1, now),
        ("Cab Express",      "cab",        "Suresh M",     "suresh@cab.com",  "Agra",    "UP",        600,  4.1, 1, 1, now),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO vendors
        (name, vendor_type, owner_name, owner_email,
         location, state, price, rating, is_verified, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', vendors)

    # Budget Plans
    budget_plans = [
        ("Student",   3000,  10000,  now),
        ("Family",    15000, 50000,  now),
        ("Luxury",    75000, 500000, now),
        ("Corporate", 30000, 150000, now),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO budget_plans
        (user_type, min_budget, max_budget, updated_at)
        VALUES (?, ?, ?, ?)
    ''', budget_plans)

    # Sample Users
    users = [
        ("Rahul Sharma",  "rahul@gmail.com",  "9876543210", "Student",   "Hindi",   8000,  5,  now),
        ("Priya Patel",   "priya@gmail.com",  "9876543211", "Family",    "Gujarati",30000, 7,  now),
        ("Amit Kumar",    "amit@gmail.com",   "9876543212", "Luxury",    "English", 150000,10, now),
        ("Sneha Reddy",   "sneha@gmail.com",  "9876543213", "Student",   "Telugu",  6000,  3,  now),
        ("Vijay Nair",    "vijay@gmail.com",  "9876543214", "Family",    "Malayalam",25000,7,  now),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO users
        (name, email, phone, user_type, language, budget, days, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', users)

    conn.commit()
    conn.close()
    print("\n✅ Sample Data Inserted Successfully!")
    print("   10 Destinations, 8 Vendors, 4 Budget Plans, 5 Users")

# =====================================
# STEP 3 - JSON TO DATABASE MIGRATE
# =====================================

def migrate_json_to_db():
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Admin config migrate karo
    try:
        with open("config/Admin_config.json", "r") as f:
            config = json.load(f)

        if config["is_setup_done"]:
            cursor.execute('''
                INSERT OR IGNORE INTO admin
                (name, username, password, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                config["admin"]["name"],
                config["admin"]["username"],
                config["admin"]["password"],
                now
            ))
            print("\n✅ Admin data migrated to database!")

        # Budget plans migrate karo
        for user_type, budget in config["budget_plans"].items():
            cursor.execute('''
                INSERT OR REPLACE INTO budget_plans
                (user_type, min_budget, max_budget, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (user_type, budget["min"], budget["max"], now))

        print("✅ Budget plans migrated to database!")

    except Exception as e:
        print(f"⚠️  Admin config migration: {e}")

    conn.commit()
    conn.close()

# =====================================
# STEP 4 - DATABASE REVIEW
# =====================================

def review_database():
    conn = connect_db()

    print("\n" + "=" * 55)
    print("  📊 DATABASE COMPLETE REVIEW")
    print("=" * 55)

    tables = ["users", "vendors", "destinations",
              "bookings", "reviews", "rewards",
              "budget_plans", "admin"]

    for table in tables:
        df = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", conn)
        count = df['count'][0]
        status = "✅" if count > 0 else "⚠️  Empty"
        print(f"  {status} {table:15} → {count} records")

    print("\n" + "=" * 55)
    print("  🌍 DESTINATIONS")
    print("=" * 55)
    df = pd.read_sql("""
        SELECT name, state, category, avg_budget
        FROM destinations
        ORDER BY avg_budget ASC
    """, conn)
    print(df.to_string(index=False))

    print("\n" + "=" * 55)
    print("  👥 REGISTERED USERS")
    print("=" * 55)
    df2 = pd.read_sql("""
        SELECT name, user_type, language, budget
        FROM users
    """, conn)
    print(df2.to_string(index=False))

    print("\n" + "=" * 55)
    print("  💰 BUDGET PLANS")
    print("=" * 55)
    df3 = pd.read_sql("""
        SELECT user_type, min_budget, max_budget
        FROM budget_plans
    """, conn)
    print(df3.to_string(index=False))

    print("\n" + "=" * 55)
    print("  🏢 VENDORS")
    print("=" * 55)
    df4 = pd.read_sql("""
        SELECT name, vendor_type, location, price, rating
        FROM vendors
        ORDER BY rating DESC
    """, conn)
    print(df4.to_string(index=False))

    conn.close()

# =====================================
# MAIN PROGRAM
# =====================================

# Step 1
create_all_tables()

# Step 2
insert_sample_data()

# Step 3
migrate_json_to_db()

# Step 4
review_database()

print("\n" + "=" * 55)
print("  🎉 DAY 7 COMPLETE!")
print("=" * 55)
print("\n  ✅ Database fully organized!")
print("  ✅ 8 tables created with proper relations!")
print("  ✅ JSON data migrated to database!")
print("  ✅ Sample data ready for ML training!")