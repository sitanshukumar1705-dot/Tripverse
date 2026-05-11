# TripVerse - Day 10 - User Segmentation & Clustering
import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  👥 TRIPVERSE - DAY 10 - USER SEGMENTATION")
print("=" * 55)

# =====================================
# DATABASE CONNECT
# =====================================
conn = sqlite3.connect("database/tripverse.db")

# =====================================
# STEP 1 - USER DATA PREPARE
# =====================================
print("\n📊 Step 1: Preparing User Dataset...")

# Synthetic user data banao
np.random.seed(42)
n_users = 200

user_data = {
    'user_id':    range(1, n_users + 1),
    'age':        np.random.randint(18, 65, n_users),
    'budget':     np.random.choice(
        [3000, 5000, 8000, 10000, 15000,
         25000, 50000, 75000, 100000],
        n_users
    ),
    'trips_taken': np.random.randint(0, 20, n_users),
    'avg_days':   np.random.randint(2, 15, n_users),
    'prefers_adventure': np.random.randint(0, 2, n_users),
    'prefers_beach':     np.random.randint(0, 2, n_users),
    'prefers_heritage':  np.random.randint(0, 2, n_users),
    'group_traveler':    np.random.randint(0, 2, n_users),
    'solo_traveler':     np.random.randint(0, 2, n_users),
}

users_df = pd.DataFrame(user_data)
print(f"✅ Dataset ready: {len(users_df)} users")
print(f"   Age range    : {users_df['age'].min()} - {users_df['age'].max()}")
print(f"   Budget range : Rs.{users_df['budget'].min():,} - Rs.{users_df['budget'].max():,}")
print(f"   Max trips    : {users_df['trips_taken'].max()}")

# =====================================
# STEP 2 - FEATURE SELECTION
# =====================================
print("\n🎯 Step 2: Selecting Features for Clustering...")

features = [
    'age', 'budget', 'trips_taken',
    'avg_days', 'prefers_adventure',
    'prefers_beach', 'prefers_heritage',
    'group_traveler', 'solo_traveler'
]

X = users_df[features]
print(f"✅ Features selected: {features}")

# =====================================
# STEP 3 - DATA SCALING
# =====================================
print("\n📏 Step 3: Scaling Data...")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("✅ Data scaled successfully!")
print("   (All features now on same scale)")

# =====================================
# STEP 4 - OPTIMAL CLUSTERS FIND KARO
# =====================================
print("\n🔍 Step 4: Finding Optimal Number of Clusters...")

inertias = []
silhouette_scores = []
k_range = range(2, 8)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    score = silhouette_score(X_scaled, kmeans.labels_)
    silhouette_scores.append(score)
    print(f"   K={k}: Inertia={kmeans.inertia_:.0f}, "
          f"Silhouette={score:.3f}")

best_k = k_range[np.argmax(silhouette_scores)]
print(f"\n✅ Optimal clusters: {best_k}")

# =====================================
# STEP 5 - KMEANS MODEL TRAIN
# =====================================
print(f"\n🤖 Step 5: Training KMeans Model (K={best_k})...")

kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
kmeans.fit(X_scaled)
users_df['cluster'] = kmeans.labels_

print("✅ Clustering complete!")

# =====================================
# STEP 6 - CLUSTER ANALYSIS
# =====================================
print("\n📊 Step 6: Analyzing Clusters...")

print("\n" + "=" * 55)
print("  USER SEGMENT ANALYSIS")
print("=" * 55)

cluster_names = {
    0: "💰 Budget Travelers",
    1: "👨‍👩‍👧 Family Travelers",
    2: "💎 Luxury Travelers",
    3: "🎒 Adventure Seekers",
    4: "🏖️  Beach Lovers",
    5: "🏛️  Heritage Explorers"
}

cluster_summary = users_df.groupby('cluster').agg(
    total_users      = ('user_id', 'count'),
    avg_age          = ('age', 'mean'),
    avg_budget       = ('budget', 'mean'),
    avg_trips        = ('trips_taken', 'mean'),
    avg_days         = ('avg_days', 'mean'),
    adventure_lovers = ('prefers_adventure', 'sum'),
    beach_lovers     = ('prefers_beach', 'sum'),
    heritage_lovers  = ('prefers_heritage', 'sum'),
    group_travelers  = ('group_traveler', 'sum'),
    solo_travelers   = ('solo_traveler', 'sum')
).round(1)

for cluster_id, row in cluster_summary.iterrows():
    name = cluster_names.get(cluster_id,
           f"Segment {cluster_id}")
    print(f"\n  {name}")
    print(f"  {'─' * 40}")
    print(f"  Total Users  : {row['total_users']:.0f}")
    print(f"  Avg Age      : {row['avg_age']:.0f} years")
    print(f"  Avg Budget   : Rs.{row['avg_budget']:,.0f}")
    print(f"  Avg Trips    : {row['avg_trips']:.1f}")
    print(f"  Avg Days     : {row['avg_days']:.1f} days")
    print(f"  Adventure    : {row['adventure_lovers']:.0f} users")
    print(f"  Beach        : {row['beach_lovers']:.0f} users")
    print(f"  Group Travel : {row['group_travelers']:.0f} users")

# =====================================
# STEP 7 - MARKETING STRATEGY
# =====================================
print("\n\n" + "=" * 55)
print("  🎯 TARGETED MARKETING STRATEGY")
print("=" * 55)

marketing_strategies = {
    0: {
        "segment": "💰 Budget Travelers",
        "strategy": [
            "Offer student group discounts",
            "Promote budget destinations (Varanasi, Agra)",
            "Hostel & shared accommodation deals",
            "Bus & train travel packages"
        ]
    },
    1: {
        "segment": "👨‍👩‍👧 Family Travelers",
        "strategy": [
            "Family package deals with kid activities",
            "Safe & comfortable hotel recommendations",
            "Kerala, Goa family tour packages",
            "Travel insurance bundle offers"
        ]
    },
    2: {
        "segment": "💎 Luxury Travelers",
        "strategy": [
            "Premium hotel & resort recommendations",
            "Private tours and concierge service",
            "Leh Ladakh, Andaman luxury packages",
            "Business class flight deals"
        ]
    },
    3: {
        "segment": "🎒 Adventure Seekers",
        "strategy": [
            "Trekking & camping packages",
            "Manali, Ladakh adventure tours",
            "Equipment rental partnerships",
            "Solo travel safety features"
        ]
    }
}

for cluster_id, info in marketing_strategies.items():
    if cluster_id < best_k:
        print(f"\n  {info['segment']}")
        print(f"  {'─' * 40}")
        for strategy in info['strategy']:
            print(f"  → {strategy}")

# =====================================
# STEP 8 - USER CLASSIFIER
# =====================================
print("\n\n" + "=" * 55)
print("  🔮 USER SEGMENT PREDICTOR")
print("=" * 55)

def predict_user_segment(age, budget, trips,
                          days, adventure, beach,
                          heritage, group, solo):
    user_features = scaler.transform([[
        age, budget, trips, days,
        adventure, beach, heritage, group, solo
    ]])
    cluster = kmeans.predict(user_features)[0]
    segment = cluster_names.get(cluster,
              f"Segment {cluster}")
    return cluster, segment

# Test predictions
test_users = [
    (22, 5000,  2, 3, 0, 0, 1, 1, 0,
     "Student - Heritage lover"),
    (35, 25000, 8, 7, 0, 1, 0, 1, 0,
     "Family - Beach lover"),
    (45, 100000, 15, 10, 0, 0, 0, 0, 0,
     "Luxury traveler"),
    (28, 8000, 5, 5, 1, 0, 0, 0, 1,
     "Solo adventure seeker"),
]

print("\n  Sample User Predictions:")
for age, budget, trips, days, adv, beach, her, grp, solo, desc in test_users:
    cluster, segment = predict_user_segment(
        age, budget, trips, days,
        adv, beach, her, grp, solo
    )
    print(f"\n  User     : {desc}")
    print(f"  Segment  : {segment}")
    print(f"  Cluster  : {cluster}")

# =====================================
# STEP 9 - VISUALIZATION
# =====================================
print("\n📊 Step 9: Generating Charts...")

if not os.path.exists("charts"):
    os.makedirs("charts")

# Chart 1 - Elbow Method + Silhouette
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(list(k_range), inertias,
             'bo-', linewidth=2, markersize=8)
axes[0].set_xlabel('Number of Clusters (K)', fontsize=12)
axes[0].set_ylabel('Inertia', fontsize=12)
axes[0].set_title('Elbow Method\n(Finding Optimal K)',
                   fontsize=13, fontweight='bold')
axes[0].axvline(x=best_k, color='red',
                linestyle='--', alpha=0.7,
                label=f'Optimal K={best_k}')
axes[0].legend()

axes[1].plot(list(k_range), silhouette_scores,
             'go-', linewidth=2, markersize=8)
axes[1].set_xlabel('Number of Clusters (K)', fontsize=12)
axes[1].set_ylabel('Silhouette Score', fontsize=12)
axes[1].set_title('Silhouette Score\n(Higher is Better)',
                   fontsize=13, fontweight='bold')
axes[1].axvline(x=best_k, color='red',
                linestyle='--', alpha=0.7,
                label=f'Best K={best_k}')
axes[1].legend()

plt.tight_layout()
plt.savefig('charts/12_optimal_clusters.png', dpi=150)
plt.close()

# Chart 2 - Cluster Distribution
cluster_counts = users_df['cluster'].value_counts().sort_index()
segment_labels = [cluster_names.get(i, f"Segment {i}")
                  for i in cluster_counts.index]
colors = ['#3498db', '#2ecc71', '#e74c3c',
          '#f39c12', '#9b59b6', '#1abc9c']

plt.figure(figsize=(12, 6))
bars = plt.bar(range(len(cluster_counts)),
               cluster_counts.values,
               color=colors[:len(cluster_counts)])
plt.xticks(range(len(cluster_counts)),
           [s.split()[0] + '\n' + s.split()[1]
            if len(s.split()) > 1 else s
            for s in segment_labels],
           fontsize=10)
plt.ylabel('Number of Users', fontsize=12)
plt.title('TripVerse - User Segment Distribution',
          fontsize=14, fontweight='bold')
for bar, count in zip(bars, cluster_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1,
             str(count), ha='center',
             va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/13_cluster_distribution.png', dpi=150)
plt.close()

# Chart 3 - Budget vs Trips scatter
plt.figure(figsize=(10, 7))
scatter_colors = [colors[c] for c in users_df['cluster']]
plt.scatter(users_df['budget'],
            users_df['trips_taken'],
            c=scatter_colors, alpha=0.6, s=50)
plt.xlabel('Budget (Rs.)', fontsize=12)
plt.ylabel('Number of Trips Taken', fontsize=12)
plt.title('TripVerse - User Clusters\n(Budget vs Trips)',
          fontsize=14, fontweight='bold')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=colors[i],
          label=cluster_names.get(i, f'Segment {i}'))
    for i in range(best_k)
]
plt.legend(handles=legend_elements, loc='upper right')
plt.tight_layout()
plt.savefig('charts/14_budget_vs_trips.png', dpi=150)
plt.close()

print("✅ 3 Charts saved!")

# =====================================
# STEP 10 - DATABASE SAVE
# =====================================
print("\n💾 Step 10: Saving to Database...")

users_df.to_sql(
    'user_segments',
    conn,
    if_exists='replace',
    index=False
)

print("✅ User segments saved to database!")
conn.close()

print("\n" + "=" * 55)
print("  🎉 DAY 10 COMPLETE!")
print("=" * 55)
print(f"\n  ✅ {n_users} Users Segmented!")
print(f"  ✅ {best_k} Optimal Clusters Found!")
print("  ✅ Marketing Strategies Generated!")
print("  ✅ User Segment Predictor Ready!")
print("  ✅ 3 Charts Generated!")
print("  ✅ Data Saved to Database!")