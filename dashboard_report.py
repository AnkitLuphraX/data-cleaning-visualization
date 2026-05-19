"""
Dashboard Report Generator - E-commerce Sales Analysis
========================================================
Author: Ankit
Date: May 2026

Creates a comprehensive visual dashboard combining multiple 
charts into a single report image, along with printing key 
insights and statistics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# load cleaned data
df = pd.read_csv('ecommerce_sales_cleaned.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

print("=" * 65)
print("   E-COMMERCE SALES ANALYSIS - KEY INSIGHTS REPORT")
print("=" * 65)

# ============================================================
# KEY METRICS
# ============================================================

total_revenue = df['total_price'].sum()
total_orders = len(df)
avg_order_value = df['total_price'].mean()
total_customers = df['customer_id'].nunique()
avg_rating = df['rating'].mean()

print(f"""
📊 KEY METRICS:
{'─' * 40}
  Total Revenue      : ₹{total_revenue:,.2f}
  Total Orders       : {total_orders:,}
  Unique Customers   : {total_customers}
  Avg Order Value    : ₹{avg_order_value:,.2f}
  Average Rating     : {avg_rating:.2f} / 5.0
""")

# ============================================================
# TOP INSIGHTS
# ============================================================

# best selling category
best_cat = df.groupby('product_category')['total_price'].sum().idxmax()
best_cat_rev = df.groupby('product_category')['total_price'].sum().max()

# best region
best_region = df.groupby('region')['total_price'].sum().idxmax()
best_region_rev = df.groupby('region')['total_price'].sum().max()

# most popular payment method
top_payment = df['payment_method'].value_counts().idxmax()

# busiest month
df['month_year'] = df['order_date'].dt.to_period('M')
busiest_month = df.groupby('month_year')['total_price'].sum().idxmax()

# highest spending age group
best_age = df.groupby('age_group')['total_price'].sum().idxmax()

print(f"""
🔍 KEY INSIGHTS:
{'─' * 40}
  1. Best Selling Category : {best_cat} (₹{best_cat_rev:,.2f})
  2. Top Revenue Region    : {best_region} (₹{best_region_rev:,.2f})
  3. Most Used Payment     : {top_payment}
  4. Peak Sales Month      : {busiest_month}
  5. Highest Spending Age  : {best_age} age group

📌 OBSERVATIONS:
{'─' * 40}
  • The {best_cat} category dominates in terms of revenue
  • {best_region} region shows the strongest market performance
  • {top_payment} is the preferred payment method
  • Customer ratings are fairly positive (avg {avg_rating:.1f}/5)
  • Discounts don't significantly impact customer satisfaction
""")

# ============================================================
# CREATE DASHBOARD IMAGE
# ============================================================

fig = plt.figure(figsize=(20, 14))
fig.suptitle('E-Commerce Sales Analysis Dashboard', fontsize=20, fontweight='bold', y=0.98)
fig.patch.set_facecolor('#f8f9fa')

# --- subplot 1: Revenue by Category ---
ax1 = fig.add_subplot(2, 3, 1)
cat_rev = df.groupby('product_category')['total_price'].sum().sort_values()
cat_rev.plot(kind='barh', ax=ax1, color=sns.color_palette("viridis", len(cat_rev)))
ax1.set_title('Revenue by Category', fontweight='bold')
ax1.set_xlabel('Revenue (₹)')
ax1.set_ylabel('')

# --- subplot 2: Monthly Trend ---
ax2 = fig.add_subplot(2, 3, 2)
monthly = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum()
ax2.plot(range(len(monthly)), monthly.values, marker='o', color='#1976D2', linewidth=2, markersize=3)
ax2.fill_between(range(len(monthly)), monthly.values, alpha=0.1, color='#1976D2')
ax2.set_title('Monthly Revenue Trend', fontweight='bold')
ax2.set_ylabel('Revenue (₹)')
ax2.set_xlabel('Month')
# only show a few tick labels
tick_pos = range(0, len(monthly), 6)
ax2.set_xticks(list(tick_pos))
ax2.set_xticklabels([str(monthly.index[i]) for i in tick_pos], rotation=45, fontsize=8)

# --- subplot 3: Region Distribution ---
ax3 = fig.add_subplot(2, 3, 3)
region_rev = df.groupby('region')['total_price'].sum()
colors_pie = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
ax3.pie(region_rev, labels=region_rev.index, autopct='%1.1f%%', colors=colors_pie, startangle=140)
ax3.set_title('Revenue by Region', fontweight='bold')

# --- subplot 4: Age Distribution ---
ax4 = fig.add_subplot(2, 3, 4)
age_order = ['18-25', '26-35', '36-45', '46-55', '56-65']
age_rev = df.groupby('age_group')['total_price'].sum().reindex(age_order)
age_rev.plot(kind='bar', ax=ax4, color=sns.color_palette("Set2", len(age_rev)))
ax4.set_title('Revenue by Age Group', fontweight='bold')
ax4.set_xlabel('Age Group')
ax4.set_ylabel('Revenue (₹)')
ax4.tick_params(axis='x', rotation=0)

# --- subplot 5: Payment Methods ---
ax5 = fig.add_subplot(2, 3, 5)
pay_counts = df['payment_method'].value_counts()
pay_counts.plot(kind='bar', ax=ax5, color=sns.color_palette("coolwarm", len(pay_counts)))
ax5.set_title('Orders by Payment Method', fontweight='bold')
ax5.set_xlabel('')
ax5.set_ylabel('Count')
ax5.tick_params(axis='x', rotation=30)

# --- subplot 6: Gender vs Spending ---
ax6 = fig.add_subplot(2, 3, 6)
gender_spend = df.groupby('gender')['total_price'].mean()
gender_spend.plot(kind='bar', ax=ax6, color=['#42A5F5', '#EF5350', '#66BB6A'])
ax6.set_title('Avg Spending by Gender', fontweight='bold')
ax6.set_xlabel('')
ax6.set_ylabel('Avg Total Price (₹)')
ax6.tick_params(axis='x', rotation=0)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('visualizations/dashboard_report.png', dpi=200, bbox_inches='tight', facecolor='#f8f9fa')
plt.close()

print("✅ Dashboard saved as 'visualizations/dashboard_report.png'")
print("\n" + "=" * 65)
print("   Report generation complete!")
print("=" * 65)
