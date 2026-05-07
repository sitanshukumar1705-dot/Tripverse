# TripVerse - Day 6 - Machine Learning
import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pickle
import os

print("=" * 50)
print("  TRIPVERSE - DAY 6 - ML MODEL")
print("=" * 50)

# =====================================
# STEP 1 - Preppearing Traing Dataset
# =====================================
print("\n Step 1: Preparing Training Dataset...")

# TripVerse ke liye synthetic travel data banate hain
np.random.seed(42)
n = 500  # 500 trips ka data

# Features jo price affect karte hain
categories    = ['Heritage', 'Beach', 'Adventure', 'Nature', 'Spiritual', 'Hills', 'City']
seasons       = ['Peak', 'Off-Peak', 'Moderate']
user_types    = ['Student', 'Family', 'Luxury']
states        = ['Rajasthan', 'Goa', 'Himachal', 'Kerala', 'UP', 'West Bengal', 'Maharashtra']

data = {
    'category':    np.random.choice(categories, n),
    'season':      np.random.choice(seasons, n),
    'user_type':   np.random.choice(user_types, n),
    'state':       np.random.choice(states, n),
    'days':        np.random.randint(2, 15, n),
    'num_people':  np.random.randint(1, 8, n),
    'has_flight':  np.random.randint(0, 2, n),
    'has_hotel':   np.random.randint(0, 2, n),
}

# Price calculate karo (realistic formula)
base_price = {
    'Heritage': 7000, 'Beach': 12000, 'Adventure': 15000,
    'Nature': 10000, 'Spiritual': 5000, 'Hills': 9000, 'City': 8000
}
season_multiplier = {'Peak': 1.4, 'Moderate': 1.0, 'Off-Peak': 0.7}
user_multiplier   = {'Student': 0.8, 'Family': 1.0, 'Luxury': 2.0}

prices = []
for i in range(n):
    price = (
        base_price[data['category'][i]] *
        season_multiplier[data['season'][i]] *
        user_multiplier[data['user_type'][i]] *
        (1 + 0.1 * data['days'][i]) *
        (1 + 0.05 * data['num_people'][i]) *
        (1 + 0.3 * data['has_flight'][i]) *
        (1 + 0.2 * data['has_hotel'][i]) +
        np.random.normal(0, 500)  # Random noise
    )
    prices.append(max(price, 1000))

data['total_price'] = prices
df = pd.DataFrame(data)

print(f" Dataset ready: {len(df)} records")
print(f"   Price range: Rs.{df['total_price'].min():,.0f} - Rs.{df['total_price'].max():,.0f}")
print(f"   Average price: Rs.{df['total_price'].mean():,.0f}")

# =====================================
# STEP 2 - DATA ENCODE KARO
# =====================================
print("\n Step 2: Data Encoding...")

df_encoded = df.copy()
le = LabelEncoder()

# Text columns ko numbers mein badlo
for col in ['category', 'season', 'user_type', 'state']:
    df_encoded[col] = le.fit_transform(df_encoded[col])

print(" Categorical data converted to numerical format!")

# =====================================
# STEP 3 - TRAIN/TEST SPLIT
# =====================================
print("\n  Step 3: Splitting Data into Train & Test Sets...")

X = df_encoded.drop('total_price', axis=1)
y = df_encoded['total_price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f" Training data: {len(X_train)} records")
print(f"   Testing data:  {len(X_test)} records")

# =====================================
# STEP 4 - MODEL TRAIN KARO
# =====================================
print("\n Step 4: Training Linear Regression Model...")

model = LinearRegression()
model.fit(X_train, y_train)

print(" Model trained successfully!")

# =====================================
# STEP 5 - MODEL EVALUATE KARO
# =====================================
print("\n Step 5: Evaluating Model Performance...")

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)

print(f" Model Performance:")
print(f"   R² Score (Accuracy): {r2:.2%}")
print(f"   Mean Absolute Error: Rs.{mae:,.0f}")

if r2 >= 0.8:
    print("    Excellent Model!")
elif r2 >= 0.6:
    print("    Good Model!")
else:
    print("    Needs Improvement!")

# =====================================
# STEP 6 - PRICE PREDICTOR FUNCTION
# =====================================
print("\n🎯 Step 6: Initializing TripVerse Price Predictor...")

def predict_price(category, season, user_type, days, num_people,
                  has_flight, has_hotel):

    cat_map  = {c: i for i, c in enumerate(sorted(categories))}
    sea_map  = {s: i for i, s in enumerate(sorted(seasons))}
    usr_map  = {u: i for i, u in enumerate(sorted(user_types))}
    sta_map  = {s: i for i, s in enumerate(sorted(states))}

    features = pd.DataFrame([[
        cat_map[category],
        sea_map[season],
        usr_map[user_type],
        sta_map['Rajasthan'],
        days, num_people,
        has_flight, has_hotel
    ]], columns=X.columns)

    price = model.predict(features)[0]
    return max(price, 1000)

# Test predictions
print("\n Sample Price Predictions:")
print("-" * 45)

trips = [
    ("Student", "Jaipur", "Heritage", "Off-Peak", 3, 4, 0, 1),
    ("Family",  "Goa",    "Beach",    "Peak",     7, 4, 1, 1),
    ("Luxury",  "Ladakh", "Adventure","Peak",    10, 2, 1, 1),
    ("Student", "Varanasi","Spiritual","Moderate", 2, 2, 0, 0),
    ("Family",  "Kerala", "Nature",   "Moderate", 5, 3, 0, 1),
]

for user, dest, cat, season, days, people, flight, hotel in trips:
    price = predict_price(cat, season, user, days, people, flight, hotel)
    flight_txt = " Flight" if flight else " Bus"
    hotel_txt  = " Hotel" if hotel else " Hostel"
    print(f"  {user:8} → {dest:10} {days} days {flight_txt} {hotel_txt}")
    print(f"            Predicted: Rs.{price:,.0f}")
    print()

# =====================================
# STEP 7 - VISUALIZATION
# =====================================
print("\n Step 7: Generating Visualization Charts...")

if not os.path.exists("charts"):
    os.makedirs("charts")

# Chart 1 - Actual vs Predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5, color='#3498db')
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Price (Rs.)', fontsize=12)
plt.ylabel('Predicted Price (Rs.)', fontsize=12)
plt.title(f'TripVerse - Actual vs Predicted Price\nR² = {r2:.2%}',
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/06_actual_vs_predicted.png', dpi=150)
plt.close()

# Chart 2 - Feature Importance
plt.figure(figsize=(10, 6))
feat_imp = pd.Series(model.coef_, index=X.columns)
feat_imp.sort_values().plot(kind='barh', color='#2ecc71')
plt.title('TripVerse - Feature Importance\n(What affects price most?)',
          fontsize=14, fontweight='bold')
plt.xlabel('Coefficient Value', fontsize=12)
plt.tight_layout()
plt.savefig('charts/07_feature_importance.png', dpi=150)
plt.close()

print(" Charts saved!")

# =====================================
# STEP 8 - MODEL SAVE KARO
# =====================================
if not os.path.exists("models"):
    os.makedirs("models")

with open("models/price_model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" Model saved: models/price_model.pkl")

print("\n" + "=" * 50)
print("  🎉 DAY 6 COMPLETE!")
print("=" * 50)
print(f"\n  Model Accuracy: {r2:.2%}")
print(f"  Price Error:    Rs.{mae:,.0f}")
print("\n   TripVerse Price Predictor Ready!")