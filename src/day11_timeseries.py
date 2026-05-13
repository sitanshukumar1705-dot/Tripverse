# TripVerse - Day 11 - Time Series & Demand Forecasting
import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  📈 TRIPVERSE - DAY 11 - TIME SERIES ANALYSIS")
print("=" * 55)

# =====================================
# DATABASE CONNECT
# =====================================
conn = sqlite3.connect("database/tripverse.db")

# =====================================
# STEP 1 - TIME SERIES DATA BANAO
# =====================================
print("\n📊 Step 1: Creating Time Series Dataset...")

np.random.seed(42)

# 24 months ka data (2 years)
months = pd.date_range(start='2024-01-01',
                       periods=24, freq='ME')

# Destination wise monthly bookings
destinations = ['Jaipur', 'Goa', 'Manali',
                'Kerala', 'Ladakh']

booking_data = {}
for dest in destinations:
    if dest == 'Goa':
        # Peak in winter (Nov-Mar)
        base = 150
        seasonal = [0.6, 0.5, 0.7, 0.4, 0.3,
                    0.2, 0.2, 0.3, 0.4, 0.6,
                    0.9, 1.0] * 2
    elif dest == 'Manali':
        # Peak in summer (Mar-Jun)
        base = 100
        seasonal = [0.3, 0.4, 0.8, 1.0, 0.9,
                    0.8, 0.5, 0.4, 0.5, 0.4,
                    0.3, 0.3] * 2
    elif dest == 'Ladakh':
        # Peak in summer (Jun-Sep)
        base = 80
        seasonal = [0.1, 0.1, 0.2, 0.3, 0.5,
                    0.9, 1.0, 0.9, 0.7, 0.3,
                    0.1, 0.1] * 2
    elif dest == 'Kerala':
        # Moderate throughout, peak in winter
        base = 120
        seasonal = [0.7, 0.6, 0.7, 0.6, 0.5,
                    0.4, 0.5, 0.5, 0.6, 0.7,
                    0.8, 0.9] * 2
    else:  # Jaipur
        # Peak in winter (Oct-Mar)
        base = 130
        seasonal = [0.8, 0.7, 0.8, 0.6, 0.4,
                    0.3, 0.3, 0.4, 0.6, 0.8,
                    0.9, 1.0] * 2

    # Trend + Seasonality + Noise
    trend = np.linspace(1.0, 1.3, 24)
    noise = np.random.normal(0, 0.05, 24)
    bookings = (base * np.array(seasonal) *
                trend + noise * base)
    booking_data[dest] = bookings.astype(int)

bookings_df = pd.DataFrame(
    booking_data, index=months
)

print(f"✅ Time series data ready!")
print(f"   Period : Jan 2024 - Dec 2025")
print(f"   Destinations: {len(destinations)}")
print(f"\n  Monthly Bookings Sample:")
print(bookings_df.head(6).to_string())

# =====================================
# STEP 2 - PRICE TIME SERIES
# =====================================
print("\n\n💰 Step 2: Price Time Series Analysis...")

# Monthly average prices
price_data = {}
for dest in destinations:
    if dest == 'Goa':
        base_price = 12000
        seasonal_factor = [0.8, 0.7, 0.9, 0.7,
                          0.6, 0.6, 0.6, 0.7,
                          0.8, 0.9, 1.2, 1.3] * 2
    elif dest == 'Manali':
        base_price = 10000
        seasonal_factor = [0.7, 0.7, 1.0, 1.2,
                          1.1, 1.0, 0.8, 0.8,
                          0.9, 0.8, 0.7, 0.7] * 2
    elif dest == 'Ladakh':
        base_price = 25000
        seasonal_factor = [0.6, 0.6, 0.7, 0.8,
                          0.9, 1.2, 1.3, 1.2,
                          1.0, 0.8, 0.6, 0.6] * 2
    else:
        base_price = 8000
        seasonal_factor = [1.1, 1.0, 1.0, 0.9,
                          0.8, 0.7, 0.7, 0.8,
                          0.9, 1.0, 1.1, 1.2] * 2

    noise = np.random.normal(0, 0.03, 24)
    prices = (base_price *
              np.array(seasonal_factor) *
              (1 + noise))
    price_data[dest] = prices.astype(int)

prices_df = pd.DataFrame(price_data, index=months)

print("✅ Price time series ready!")

# =====================================
# STEP 3 - SEASONAL DECOMPOSITION
# =====================================
print("\n🔍 Step 3: Seasonal Decomposition...")

print("\n  Goa Booking Decomposition:")
goa_series = bookings_df['Goa']
decomposition = seasonal_decompose(
    goa_series,
    model='multiplicative',
    period=12
)

print(f"  Trend    : Min={decomposition.trend.dropna().min():.0f}"
      f" Max={decomposition.trend.dropna().max():.0f}")
print(f"  Seasonal : Min={decomposition.seasonal.min():.2f}"
      f" Max={decomposition.seasonal.max():.2f}")
print(f"  Residual : Min={decomposition.resid.dropna().min():.2f}"
      f" Max={decomposition.resid.dropna().max():.2f}")

# =====================================
# STEP 4 - DEMAND FORECASTING
# =====================================
print("\n🔮 Step 4: Demand Forecasting...")

def forecast_bookings(dest_series, dest_name, periods=6):
    model = ExponentialSmoothing(
        dest_series,
        trend='add',
        seasonal='add',
        seasonal_periods=12
    )
    fitted = model.fit(optimized=True)
    forecast = fitted.forecast(periods)

    print(f"\n  📍 {dest_name} - Next {periods} Months Forecast:")
    print(f"  {'Month':<15} {'Forecast':>10} {'vs Avg':>10}")
    print(f"  {'─'*35}")

    avg_bookings = dest_series.mean()
    future_months = pd.date_range(
        start=dest_series.index[-1] + pd.DateOffset(months=1),
        periods=periods,
        freq='ME'
    )

    for month, value in zip(future_months, forecast):
        change = ((value - avg_bookings) / avg_bookings) * 100
        trend = "📈" if change > 0 else "📉"
        print(f"  {month.strftime('%b %Y'):<15}"
              f" {max(0, int(value)):>10}"
              f" {trend} {change:>+.1f}%")

    return forecast

# Forecast for each destination
all_forecasts = {}
for dest in destinations:
    forecast = forecast_bookings(
        bookings_df[dest], dest
    )
    all_forecasts[dest] = forecast

# =====================================
# STEP 5 - PEAK SEASON ANALYSIS
# =====================================
print("\n\n" + "=" * 55)
print("  📅 PEAK SEASON ANALYSIS")
print("=" * 55)

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for dest in destinations:
    monthly_avg = []
    for month_num in range(1, 13):
        mask = bookings_df.index.month == month_num
        avg = bookings_df.loc[mask, dest].mean()
        monthly_avg.append(avg)

    peak_month = month_names[np.argmax(monthly_avg)]
    low_month  = month_names[np.argmin(monthly_avg)]
    peak_val   = max(monthly_avg)
    low_val    = min(monthly_avg)

    print(f"\n  📍 {dest}")
    print(f"     Peak Month : {peak_month}"
          f" ({peak_val:.0f} bookings)")
    print(f"     Low Month  : {low_month}"
          f" ({low_val:.0f} bookings)")
    print(f"     Seasonality: {((peak_val/low_val)-1)*100:.0f}%"
          f" variation")

# =====================================
# STEP 6 - PRICE TREND ANALYSIS
# =====================================
print("\n\n" + "=" * 55)
print("  💰 PRICE TREND ANALYSIS")
print("=" * 55)

print("\n  Best Time to Book (Cheapest Month):")
for dest in destinations:
    monthly_price = []
    for month_num in range(1, 13):
        mask = prices_df.index.month == month_num
        avg = prices_df.loc[mask, dest].mean()
        monthly_price.append(avg)

    cheap_month   = month_names[np.argmin(monthly_price)]
    expensive_month = month_names[np.argmax(monthly_price)]
    min_price     = min(monthly_price)
    max_price     = max(monthly_price)
    savings       = max_price - min_price

    print(f"\n  📍 {dest}")
    print(f"     Cheapest   : {cheap_month}"
          f" (Rs.{min_price:,.0f})")
    print(f"     Most Exp.  : {expensive_month}"
          f" (Rs.{max_price:,.0f})")
    print(f"     Max Savings: Rs.{savings:,.0f}")

# =====================================
# STEP 7 - REVENUE ANALYSIS
# =====================================
print("\n\n" + "=" * 55)
print("  📊 REVENUE ANALYSIS")
print("=" * 55)

revenue_df = bookings_df * prices_df
total_revenue = revenue_df.sum()

print("\n  Total Revenue by Destination (2 Years):")
for dest in destinations:
    rev = total_revenue[dest]
    print(f"  {dest:<12}: Rs.{rev:>15,.0f}")

print(f"\n  Total Platform Revenue: "
      f"Rs.{total_revenue.sum():,.0f}")

# =====================================
# STEP 8 - SMART ALERTS
# =====================================
print("\n\n" + "=" * 55)
print("  🔔 SMART BOOKING ALERTS")
print("=" * 55)

print("\n  Current Month Recommendations:")
current_month = 5  # May

for dest in destinations:
    monthly_avg = []
    for m in range(1, 13):
        mask = bookings_df.index.month == m
        avg = bookings_df.loc[mask, dest].mean()
        monthly_avg.append(avg)

    overall_avg = np.mean(monthly_avg)
    current_bookings = monthly_avg[current_month - 1]

    if current_bookings > overall_avg * 1.2:
        alert = "🔴 Peak Season - Book Early!"
        advice = "Prices are high - book ASAP!"
    elif current_bookings < overall_avg * 0.8:
        alert = "🟢 Off Season - Great Deals!"
        advice = "Best time for budget travel!"
    else:
        alert = "🟡 Moderate Season"
        advice = "Good time to plan trip!"

    print(f"\n  {dest}: {alert}")
    print(f"  Advice: {advice}")

# =====================================
# STEP 9 - VISUALIZATION
# =====================================
print("\n📊 Step 9: Generating Charts...")

if not os.path.exists("charts"):
    os.makedirs("charts")

# Chart 1 - Booking Trends
plt.figure(figsize=(14, 7))
colors = ['#3498db', '#e74c3c', '#2ecc71',
          '#f39c12', '#9b59b6']
for i, dest in enumerate(destinations):
    plt.plot(bookings_df.index,
             bookings_df[dest],
             label=dest,
             color=colors[i],
             linewidth=2)

plt.title('TripVerse - Monthly Booking Trends\n(2024-2025)',
          fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Number of Bookings', fontsize=12)
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('charts/15_booking_trends.png', dpi=150)
plt.close()

# Chart 2 - Price Trends
plt.figure(figsize=(14, 7))
for i, dest in enumerate(destinations):
    plt.plot(prices_df.index,
             prices_df[dest],
             label=dest,
             color=colors[i],
             linewidth=2)

plt.title('TripVerse - Monthly Price Trends\n(2024-2025)',
          fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Price (Rs.)', fontsize=12)
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('charts/16_price_trends.png', dpi=150)
plt.close()

# Chart 3 - Revenue Comparison
plt.figure(figsize=(10, 6))
rev_values = [total_revenue[d] for d in destinations]
bars = plt.bar(destinations, rev_values,
               color=colors)
plt.title('TripVerse - Total Revenue by Destination\n(2 Years)',
          fontsize=14, fontweight='bold')
plt.ylabel('Total Revenue (Rs.)', fontsize=12)
for bar, val in zip(bars, rev_values):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 500000,
             f'Rs.{val/1000000:.1f}M',
             ha='center', fontsize=9,
             fontweight='bold')
plt.tight_layout()
plt.savefig('charts/17_revenue_comparison.png', dpi=150)
plt.close()

# Chart 4 - Seasonal Heatmap
fig, ax = plt.subplots(figsize=(14, 6))
seasonal_matrix = np.zeros((len(destinations), 12))

for i, dest in enumerate(destinations):
    for m in range(12):
        mask = bookings_df.index.month == (m + 1)
        seasonal_matrix[i, m] = bookings_df.loc[
            mask, dest
        ].mean()

im = ax.imshow(seasonal_matrix,
               cmap='YlOrRd', aspect='auto')
ax.set_xticks(range(12))
ax.set_xticklabels(month_names)
ax.set_yticks(range(len(destinations)))
ax.set_yticklabels(destinations)
plt.colorbar(im, label='Avg Monthly Bookings')
ax.set_title('TripVerse - Seasonal Booking Heatmap',
             fontsize=14, fontweight='bold')

for i in range(len(destinations)):
    for j in range(12):
        ax.text(j, i,
                f'{seasonal_matrix[i,j]:.0f}',
                ha='center', va='center',
                fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/18_seasonal_heatmap.png', dpi=150)
plt.close()

print("✅ 4 Charts saved!")

# =====================================
# STEP 10 - DATABASE SAVE
# =====================================
print("\n💾 Step 10: Saving to Database...")

bookings_df_save = bookings_df.reset_index()
bookings_df_save.columns = (
    ['date'] + list(bookings_df.columns)
)
bookings_df_save['date'] = bookings_df_save[
    'date'
].astype(str)
bookings_df_save.to_sql(
    'booking_trends',
    conn,
    if_exists='replace',
    index=False
)

prices_df_save = prices_df.reset_index()
prices_df_save.columns = (
    ['date'] + list(prices_df.columns)
)
prices_df_save['date'] = prices_df_save[
    'date'
].astype(str)
prices_df_save.to_sql(
    'price_trends',
    conn,
    if_exists='replace',
    index=False
)

print("✅ Booking & Price trends saved!")
conn.close()

print("\n" + "=" * 55)
print("  🎉 DAY 11 COMPLETE!")
print("=" * 55)
print("\n  ✅ 24 Months Time Series Created!")
print("  ✅ Seasonal Decomposition Done!")
print("  ✅ 6 Month Demand Forecast Ready!")
print("  ✅ Peak Season Analysis Done!")
print("  ✅ Price Trend Analysis Done!")
print("  ✅ Smart Booking Alerts Ready!")
print("  ✅ 4 Charts Generated!")
print("  ✅ Data Saved to Database!")