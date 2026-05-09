# TripVerse - Day 8 - Recommendation System
import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  🤖 TRIPVERSE - DAY 8 - RECOMMENDATION SYSTEM")
print("=" * 55)

# =====================================
# DATABASE CONNECT
# =====================================
conn = sqlite3.connect("database/tripverse.db")

# =====================================
# STEP 1 - DATA LOAD KARO
# =====================================
print("\n📊 Step 1: Loading Data from Database...")

destinations_df = pd.read_sql("SELECT * FROM destinations", conn)
users_df = pd.read_sql("SELECT * FROM users", conn)
vendors_df = pd.read_sql("SELECT * FROM vendors", conn)
print(f"✅ Loaded: {len(destinations_df)} destinations, {len(users_df)} users, {len(vendors_df)} vendors")

# =====================================
# STEP 2 - CONTENT BASED FILTERING
# =====================================
print("\n🎯 Step 2: Content Based Recommendation...")

def content_based_recommend(user_type, budget, days):
    df = destinations_df.copy()

    # Budget filter
    if user_type == "Student":
        df = df[df['avg_budget'] <= 10000]
    elif user_type == "Family":
        df = df[(df['avg_budget'] >= 8000) & (df['avg_budget'] <= 30000)]
    elif user_type == "Luxury":
        df = df[df['avg_budget'] >= 15000]

    # Budget match score
    df['budget_score'] = 1 - abs(df['avg_budget'] - budget) / budget
    df['budget_score'] = df['budget_score'].clip(0, 1)

    # Sort by score
    df = df.sort_values('budget_score', ascending=False)

    return df[['name', 'state', 'category', 'avg_budget', 'budget_score']].head(3)

# Test karo
print("\n  Recommendations for Different Users:")
print("\n  🎒 Student (Budget: Rs.8000, 5 days):")
result1 = content_based_recommend("Student", 8000, 5)
print(result1.to_string(index=False))

print("\n  👨‍👩‍👧 Family (Budget: Rs.25000, 7 days):")
result2 = content_based_recommend("Family", 25000, 7)
print(result2.to_string(index=False))

print("\n  💎 Luxury (Budget: Rs.100000, 10 days):")
result3 = content_based_recommend("Luxury", 100000, 10)
print(result3.to_string(index=False))

# =====================================
# STEP 3 - COLLABORATIVE FILTERING
# =====================================
print("\n👥 Step 3: Collaborative Filtering...")

# Synthetic user-destination ratings banao
np.random.seed(42)
user_names = ["Rahul", "Priya", "Amit", "Sneha", "Vijay",
              "Ravi", "Anita", "Suresh", "Meera", "Kiran"]
dest_names = list(destinations_df['name'])

# Rating matrix (0 = nahi gaya, 1-5 = rating)
ratings = np.random.choice(
    [0, 0, 0, 1, 2, 3, 4, 5],
    size=(len(user_names), len(dest_names))
)
ratings_df = pd.DataFrame(
    ratings,
    index=user_names,
    columns=dest_names
)

print("✅ User-Destination Rating Matrix:")
print(ratings_df.to_string())

# Cosine Similarity calculate karo
user_similarity = cosine_similarity(ratings_df)
user_sim_df = pd.DataFrame(
    user_similarity,
    index=user_names,
    columns=user_names
)

def collaborative_recommend(user_name, top_n=3):
    if user_name not in user_sim_df.index:
        return []

    # Similar users dhundho
    similar_users = user_sim_df[user_name].sort_values(
        ascending=False
    )[1:4]

    # Un users ki top destinations
    recommendations = []
    for sim_user, sim_score in similar_users.items():
        user_ratings = ratings_df.loc[sim_user]
        top_dest = user_ratings[user_ratings > 3].sort_values(
            ascending=False
        ).head(2)
        for dest, rating in top_dest.items():
            if ratings_df.loc[user_name, dest] == 0:
                recommendations.append({
                    'destination': dest,
                    'similar_user': sim_user,
                    'similarity': round(sim_score, 2),
                    'rating': rating
                })

    rec_df = pd.DataFrame(recommendations).drop_duplicates(
        subset=['destination']
    ).head(top_n)
    return rec_df

print("\n  Collaborative Recommendations:")
print("\n  For Rahul:")
rec = collaborative_recommend("Rahul")
if len(rec) > 0:
    print(rec.to_string(index=False))

print("\n  For Priya:")
rec2 = collaborative_recommend("Priya")
if len(rec2) > 0:
    print(rec2.to_string(index=False))

# =====================================
# STEP 4 - VENDOR RECOMMENDATION
# =====================================
print("\n🏢 Step 4: Vendor Recommendation...")

def recommend_vendors(destination, vendor_type=None):
    df = vendors_df.copy()
    df = df[df['location'] == destination]

    if vendor_type:
        df = df[df['vendor_type'] == vendor_type]

    df = df.sort_values('rating', ascending=False)
    return df[['name', 'vendor_type', 'price', 'rating']].head(3)

print("\n  Top Vendors for Goa:")
goa_vendors = recommend_vendors("Goa")
if len(goa_vendors) > 0:
    print(goa_vendors.to_string(index=False))
else:
    print("  No vendors found for Goa")

print("\n  Top Hotels for Jaipur:")
jaipur_hotels = recommend_vendors("Jaipur", "hotel")
if len(jaipur_hotels) > 0:
    print(jaipur_hotels.to_string(index=False))
else:
    print("  No hotels found for Jaipur")

# =====================================
# STEP 5 - SMART TRIP PLANNER
# =====================================
print("\n🗺️  Step 5: Smart Trip Planner...")

def smart_trip_plan(user_type, budget, days, preference=None):
    print(f"\n  {'='*45}")
    print(f"  🌍 TRIPVERSE SMART TRIP PLAN")
    print(f"  {'='*45}")
    print(f"  User Type  : {user_type}")
    print(f"  Budget     : Rs.{budget:,}")
    print(f"  Days       : {days}")
    if preference:
        print(f"  Preference : {preference}")

    # Best destinations
    dest_df = destinations_df.copy()
    if preference:
        dest_df = dest_df[dest_df['category'] == preference]

    dest_df['score'] = 1 - abs(
        dest_df['avg_budget'] - budget
    ) / budget
    dest_df['score'] = dest_df['score'].clip(0, 1)
    best_dest = dest_df.sort_values(
        'score', ascending=False
    ).iloc[0]

    print(f"\n  📍 Recommended Destination:")
    print(f"     {best_dest['name']}, {best_dest['state']}")
    print(f"     Category   : {best_dest['category']}")
    print(f"     Est. Budget: Rs.{best_dest['avg_budget']:,}")
    print(f"     Best Season: {best_dest['best_season']}")

    # Best vendors
    dest_vendors = vendors_df[
        vendors_df['location'] == best_dest['name']
    ]

    if len(dest_vendors) > 0:
        print(f"\n  🏨 Recommended Services:")
        for _, vendor in dest_vendors.iterrows():
            print(f"     {vendor['vendor_type'].title():12}: "
                  f"{vendor['name']} "
                  f"(Rs.{vendor['price']:,}/night, "
                  f"⭐{vendor['rating']})")

    # Budget breakdown
    hotel_cost = best_dest['avg_budget'] * 0.4
    food_cost  = best_dest['avg_budget'] * 0.2
    travel_cost = best_dest['avg_budget'] * 0.3
    misc_cost  = best_dest['avg_budget'] * 0.1

    print(f"\n  💰 Estimated Budget Breakdown:")
    print(f"     Hotel/Stay : Rs.{hotel_cost:,.0f}")
    print(f"     Food       : Rs.{food_cost:,.0f}")
    print(f"     Travel     : Rs.{travel_cost:,.0f}")
    print(f"     Misc       : Rs.{misc_cost:,.0f}")
    print(f"     {'─'*30}")
    print(f"     Total      : Rs.{best_dest['avg_budget']:,}")

# Test Smart Planner
smart_trip_plan("Student", 8000, 5, "Heritage")
smart_trip_plan("Family", 25000, 7, "Beach")
smart_trip_plan("Luxury", 100000, 10, "Adventure")

# =====================================
# STEP 6 - VISUALIZATION
# =====================================
print("\n📊 Step 6: Generating Charts...")

# Chart 1 - User Similarity Heatmap
plt.figure(figsize=(10, 8))
plt.imshow(user_similarity, cmap='YlOrRd', aspect='auto')
plt.colorbar(label='Similarity Score')
plt.xticks(range(len(user_names)), user_names, rotation=45)
plt.yticks(range(len(user_names)), user_names)
plt.title('TripVerse - User Similarity Matrix\n(Collaborative Filtering)',
          fontsize=14, fontweight='bold')
for i in range(len(user_names)):
    for j in range(len(user_names)):
        plt.text(j, i, f'{user_similarity[i,j]:.1f}',
                ha='center', va='center', fontsize=7)
plt.tight_layout()
plt.savefig('charts/08_user_similarity.png', dpi=150)
plt.close()

# Chart 2 - Destination Score Chart
dest_scores = destinations_df.copy()
dest_scores['match_score'] = 1 - abs(
    dest_scores['avg_budget'] - 8000
) / 8000
dest_scores['match_score'] = dest_scores['match_score'].clip(0,1)
dest_scores = dest_scores.sort_values('match_score', ascending=True)

plt.figure(figsize=(10, 6))
colors = ['#2ecc71' if s >= 0.7 else '#f39c12' if s >= 0.4
          else '#e74c3c' for s in dest_scores['match_score']]
plt.barh(dest_scores['name'], dest_scores['match_score'], color=colors)
plt.title('TripVerse - Destination Match Score\n(Student Budget: Rs.8,000)',
          fontsize=14, fontweight='bold')
plt.xlabel('Match Score (0-1)', fontsize=12)
plt.axvline(x=0.7, color='green', linestyle='--',
            alpha=0.7, label='Good Match (0.7+)')
plt.legend()
plt.tight_layout()
plt.savefig('charts/09_destination_match.png', dpi=150)
plt.close()

print("✅ Charts saved!")

conn.close()

print("\n" + "=" * 55)
print("  🎉 DAY 8 COMPLETE!")
print("=" * 55)
print("\n  ✅ Content Based Filtering Ready!")
print("  ✅ Collaborative Filtering Ready!")
print("  ✅ Vendor Recommendation Ready!")
print("  ✅ Smart Trip Planner Ready!")
print("  ✅ 2 New Charts Generated!")