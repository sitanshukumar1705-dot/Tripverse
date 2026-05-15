# TripVerse - Day 9 - Sentiment Analysis & NLP
import sqlite3
import pandas as pd
import numpy as np
from textblob import TextBlob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  📝 TRIPVERSE - DAY 9 - SENTIMENT ANALYSIS")
print("=" * 55)

# =====================================
# DATABASE CONNECT
# =====================================
conn = sqlite3.connect("database/tripverse.db")

# =====================================
# STEP 1 - SAMPLE REVIEWS BANAO
# =====================================
print("\n📊 Step 1: Creating Sample Reviews Dataset...")

reviews_data = [
    # Hotel Reviews
    ("Hotel Taj", "hotel", "Jaipur",
     "Absolutely amazing experience! The rooms were luxurious and staff was very helpful. Best hotel in Jaipur!", 5),
    ("Hotel Taj", "hotel", "Jaipur",
     "Good hotel but a bit expensive. Room service was excellent though.", 4),
    ("Hotel Taj", "hotel", "Jaipur",
     "Terrible experience! Room was dirty and staff was rude. Never coming back!", 1),
    ("Beach Resort", "hotel", "Goa",
     "Perfect beach view! Loved every moment of our stay. Highly recommended!", 5),
    ("Beach Resort", "hotel", "Goa",
     "Average hotel. Nothing special. Food could have been better.", 3),

    # Restaurant Reviews
    ("Spice Kitchen", "restaurant", "Goa",
     "Outstanding food! The spices were perfect and ambiance was wonderful.", 5),
    ("Spice Kitchen", "restaurant", "Goa",
     "Good food but service was slow. Had to wait 45 minutes for order.", 3),
    ("Spice Kitchen", "restaurant", "Goa",
     "Worst food ever! Completely tasteless and overpriced. Very disappointed.", 1),

    # Adventure Reviews
    ("Trek Adventures", "adventure", "Ladakh",
     "Incredible trek experience! Guide was knowledgeable and safety measures were top notch.", 5),
    ("Trek Adventures", "adventure", "Ladakh",
     "Amazing adventure but very physically demanding. Not for beginners!", 4),
    ("Trek Adventures", "adventure", "Ladakh",
     "Excellent organization and beautiful scenery. Will definitely come back!", 5),

    # Homestay Reviews
    ("Kerala Homestay", "homestay", "Kerala",
     "Felt like home! Host family was wonderful and food was authentic Kerala cuisine.", 5),
    ("Kerala Homestay", "homestay", "Kerala",
     "Good experience overall. Location was perfect near backwaters.", 4),
    ("Kerala Homestay", "homestay", "Kerala",
     "Disappointing stay. No hot water and WiFi was not working.", 2),

    # Bus Reviews
    ("Volvo Travels", "bus", "Manali",
     "Comfortable journey! Bus was clean and driver was professional.", 4),
    ("Volvo Travels", "bus", "Manali",
     "Terrible bus service! Delay of 3 hours and no AC was working.", 1),
    ("Volvo Travels", "bus", "Manali",
     "Decent service for the price. Could improve on punctuality.", 3),

    # Cab Reviews
    ("Cab Express", "cab", "Agra",
     "Driver was very friendly and knew all historical places. Great experience!", 5),
    ("Cab Express", "cab", "Agra",
     "Okay service. Car was clean but driver did not speak English.", 3),
]

reviews_df = pd.DataFrame(reviews_data, columns=[
    'vendor_name', 'vendor_type', 'location',
    'review_text', 'rating'
])

print(f"✅ Created {len(reviews_df)} sample reviews!")

# =====================================
# STEP 2 - TEXT CLEANING
# =====================================
print("\n🧹 Step 2: Cleaning Review Text...")

def clean_text(text):
    # Lowercase karo
    text = text.lower()
    # Special characters hatao
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Extra spaces hatao
    text = re.sub(r'\s+', ' ', text).strip()
    return text

reviews_df['clean_text'] = reviews_df['review_text'].apply(clean_text)

print("✅ Text cleaning complete!")
print("\n  Original vs Cleaned:")
print(f"  Original : {reviews_df['review_text'][0][:50]}...")
print(f"  Cleaned  : {reviews_df['clean_text'][0][:50]}...")

# =====================================
# STEP 3 - SENTIMENT ANALYSIS
# =====================================
print("\n🎭 Step 3: Performing Sentiment Analysis...")

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = "Positive 😊"
    elif polarity < -0.1:
        sentiment = "Negative 😞"
    else:
        sentiment = "Neutral 😐"

    return polarity, subjectivity, sentiment

# Apply sentiment analysis
results = reviews_df['clean_text'].apply(
    lambda x: analyze_sentiment(x)
)
reviews_df['polarity']     = results.apply(lambda x: x[0])
reviews_df['subjectivity'] = results.apply(lambda x: x[1])
reviews_df['sentiment']    = results.apply(lambda x: x[2])

print("✅ Sentiment Analysis Complete!")

# =====================================
# STEP 4 - RESULTS SHOW KARO
# =====================================
print("\n📊 Step 4: Analysis Results...")

print("\n" + "=" * 55)
print("  SENTIMENT ANALYSIS RESULTS")
print("=" * 55)

for _, row in reviews_df.iterrows():
    print(f"\n  Vendor   : {row['vendor_name']}")
    print(f"  Review   : {row['review_text'][:60]}...")
    print(f"  Rating   : {'⭐' * row['rating']}")
    print(f"  Sentiment: {row['sentiment']}")
    print(f"  Polarity : {row['polarity']:.2f}")

# =====================================
# STEP 5 - VENDOR WISE ANALYSIS
# =====================================
print("\n\n" + "=" * 55)
print("  📈 VENDOR WISE SENTIMENT SUMMARY")
print("=" * 55)

vendor_analysis = reviews_df.groupby('vendor_name').agg(
    total_reviews  = ('review_text', 'count'),
    avg_rating     = ('rating', 'mean'),
    avg_polarity   = ('polarity', 'mean'),
    positive_count = ('sentiment', lambda x: (x == 'Positive 😊').sum()),
    negative_count = ('sentiment', lambda x: (x == 'Negative 😞').sum()),
    neutral_count  = ('sentiment', lambda x: (x == 'Neutral 😐').sum())
).round(2)

print(vendor_analysis.to_string())

# =====================================
# STEP 6 - SENTIMENT DISTRIBUTION
# =====================================
print("\n\n" + "=" * 55)
print("  📊 OVERALL SENTIMENT DISTRIBUTION")
print("=" * 55)

sentiment_counts = reviews_df['sentiment'].value_counts()
total = len(reviews_df)

for sentiment, count in sentiment_counts.items():
    percentage = (count / total) * 100
    bar = "█" * int(percentage / 5)
    print(f"  {sentiment:20} {bar} {count} ({percentage:.1f}%)")

# =====================================
# STEP 7 - KEYWORD ANALYSIS
# =====================================
print("\n\n" + "=" * 55)
print("  🔑 KEYWORD ANALYSIS")
print("=" * 55)

positive_reviews = reviews_df[
    reviews_df['sentiment'] == 'Positive 😊'
]['clean_text']
negative_reviews = reviews_df[
    reviews_df['sentiment'] == 'Negative 😞'
]['clean_text']

# Common words
stop_words = {'was', 'the', 'and', 'for', 'but',
              'our', 'had', 'to', 'of', 'a', 'an',
              'in', 'on', 'at', 'is', 'it', 'be',
              'are', 'were', 'have', 'has', 'not'}

def get_top_words(texts, n=5):
    all_words = ' '.join(texts).split()
    word_freq = {}
    for word in all_words:
        if word not in stop_words and len(word) > 3:
            word_freq[word] = word_freq.get(word, 0) + 1
    return sorted(word_freq.items(),
                  key=lambda x: x[1], reverse=True)[:n]

print("\n  ✅ Top Positive Keywords:")
for word, count in get_top_words(positive_reviews):
    print(f"     '{word}' → {count} times")

print("\n  ❌ Top Negative Keywords:")
for word, count in get_top_words(negative_reviews):
    print(f"     '{word}' → {count} times")

# =====================================
# STEP 8 - FAKE REVIEW DETECTION
# =====================================
print("\n\n" + "=" * 55)
print("  🔍 FAKE REVIEW DETECTION")
print("=" * 55)

def detect_fake_review(polarity, subjectivity, rating):
    # Highly subjective + extreme polarity = suspicious
    if subjectivity > 0.8 and abs(polarity) > 0.8:
        if (polarity > 0 and rating < 3) or \
           (polarity < 0 and rating > 3):
            return "⚠️  Suspicious - Rating & Sentiment Mismatch"

    if subjectivity > 0.9:
        return "⚠️  Suspicious - Highly Subjective"

    return "✅ Genuine Review"

reviews_df['review_status'] = reviews_df.apply(
    lambda row: detect_fake_review(
        row['polarity'],
        row['subjectivity'],
        row['rating']
    ), axis=1
)

suspicious = reviews_df[
    reviews_df['review_status'].str.contains('Suspicious')
]

print(f"\n  Total Reviews   : {len(reviews_df)}")
print(f"  Genuine Reviews : "
      f"{len(reviews_df) - len(suspicious)}")
print(f"  Suspicious      : {len(suspicious)}")

if len(suspicious) > 0:
    print("\n  Suspicious Reviews:")
    for _, row in suspicious.iterrows():
        print(f"\n  ⚠️  {row['vendor_name']}")
        print(f"     Review : {row['review_text'][:50]}...")
        print(f"     Status : {row['review_status']}")

# =====================================
# STEP 9 - VISUALIZATION
# =====================================
print("\n📊 Step 9: Generating Charts...")

if not os.path.exists("charts"):
    os.makedirs("charts")

# Chart 1 - Sentiment Distribution Pie
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sentiment_counts = reviews_df['sentiment'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#95a5a6']
axes[0].pie(sentiment_counts.values,
            labels=[s.split()[0] for s in sentiment_counts.index],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            shadow=True)
axes[0].set_title('TripVerse - Sentiment Distribution',
                  fontsize=13, fontweight='bold')

# Chart 2 - Vendor Polarity
vendor_pol = reviews_df.groupby('vendor_name')['polarity'].mean()
colors2 = ['#2ecc71' if p > 0.1 else '#e74c3c' if p < -0.1
           else '#95a5a6' for p in vendor_pol.values]
axes[1].barh(vendor_pol.index, vendor_pol.values, color=colors2)
axes[1].axvline(x=0, color='black', linestyle='-', linewidth=0.5)
axes[1].set_title('TripVerse - Vendor Sentiment Score',
                  fontsize=13, fontweight='bold')
axes[1].set_xlabel('Sentiment Polarity (-1 to +1)')

plt.tight_layout()
plt.savefig('charts/10_sentiment_analysis.png', dpi=150)
plt.close()

# Chart 2 - Rating vs Polarity
plt.figure(figsize=(10, 6))
colors3 = ['#2ecc71' if s == 'Positive 😊'
           else '#e74c3c' if s == 'Negative 😞'
           else '#95a5a6'
           for s in reviews_df['sentiment']]
plt.scatter(reviews_df['rating'],
            reviews_df['polarity'],
            c=colors3, s=100, alpha=0.7)
plt.xlabel('User Rating (1-5)', fontsize=12)
plt.ylabel('Sentiment Polarity (-1 to +1)', fontsize=12)
plt.title('TripVerse - Rating vs Sentiment Polarity',
          fontsize=14, fontweight='bold')
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('charts/11_rating_vs_sentiment.png', dpi=150)
plt.close()

print("✅ Charts saved!")

# =====================================
# STEP 10 - DATABASE Save
# =====================================
print("\n💾 Step 10: Saving to Database...")

reviews_df_db = reviews_df[[
    'vendor_name', 'vendor_type', 'location',
    'review_text', 'rating', 'polarity',
    'subjectivity', 'sentiment'
]].copy()

reviews_df_db.to_sql(
    'sentiment_reviews',
    conn,
    if_exists='replace',
    index=False
)

print("✅ Reviews saved to database!")

conn.close()

print("\n" + "=" * 55)
print("  🎉 DAY 9 COMPLETE!")
print("=" * 55)
print("\n  ✅ 19 Reviews Analyzed!")
print("  ✅ Sentiment Analysis Done!")
print("  ✅ Keyword Analysis Done!")
print("  ✅ Fake Review Detection Done!")
print("  ✅ 2 Charts Generated!")
print("  ✅ Data Saved to Database!")