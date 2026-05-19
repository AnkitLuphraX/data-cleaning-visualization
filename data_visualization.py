"""
Data Visualization Script - E-commerce Sales Dataset
======================================================
Author: Ankit
Date: May 2026

This script creates various visualizations from the cleaned dataset
to identify trends, patterns, and key insights.

Charts created:
  1. Sales distribution by category
  2. Monthly revenue trend
  3. Customer age distribution
  4. Region-wise performance
  5. Payment method analysis
  6. Correlation heatmap
  7. Top customers
  8. Discount impact analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# set up styling
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# create output directory for saving charts
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')
    print("Created 'visualizations/' folder")

# load cleaned data
df = pd.read_csv('ecommerce_sales_cleaned.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

print(f"Loaded cleaned dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print("Starting visualization...\n")

# ============================================================
# CHART 1: Sales by Product Category (Bar Chart)
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# total revenue per category
category_revenue = df.groupby('product_category')['total_price'].sum().sort_values(ascending=True)
colors = sns.color_palette("viridis", len(category_revenue))
category_revenue.plot(kind='barh', ax=axes[0], color=colors)
axes[0].set_title('Total Revenue by Category')
axes[0].set_xlabel('Revenue (₹)')
axes[0].set_ylabel('')

# order count per category
category_count = df['product_category'].value_counts().sort_values(ascending=True)
category_count.plot(kind='barh', ax=axes[1], color=sns.color_palette("magma", len(category_count)))
axes[1].set_title('Number of Orders by Category')
axes[1].set_xlabel('Order Count')
axes[1].set_ylabel('')

plt.tight_layout()
plt.savefig('visualizations/01_category_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 1 saved: Category Analysis")

# ============================================================
# CHART 2: Monthly Revenue Trend (Line Chart)
# ============================================================

fig, ax = plt.subplots(figsize=(14, 6))

monthly_revenue = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum()
monthly_revenue.index = monthly_revenue.index.astype(str)

# plot with markers
ax.plot(range(len(monthly_revenue)), monthly_revenue.values, 
        marker='o', linewidth=2, markersize=5, color='#2196F3')
ax.fill_between(range(len(monthly_revenue)), monthly_revenue.values, alpha=0.15, color='#2196F3')
ax.set_title('Monthly Revenue Trend (2023-2024)')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue (₹)')

# show every 3rd label to avoid crowding
tick_positions = range(0, len(monthly_revenue), 3)
ax.set_xticks(tick_positions)
ax.set_xticklabels([monthly_revenue.index[i] for i in tick_positions], rotation=45, ha='right')

plt.tight_layout()
plt.savefig('visualizations/02_monthly_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 2 saved: Monthly Revenue Trend")

# ============================================================
# CHART 3: Customer Age Distribution
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# histogram
axes[0].hist(df['customer_age'], bins=20, color='#FF7043', edgecolor='white', alpha=0.85)
axes[0].set_title('Age Distribution of Customers')
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Frequency')
axes[0].axvline(df['customer_age'].mean(), color='red', linestyle='--', label=f"Mean: {df['customer_age'].mean():.0f}")
axes[0].legend()

# age group spending (box plot)
age_group_order = ['18-25', '26-35', '36-45', '46-55', '56-65']
df_plot = df.copy()
df_plot['age_group'] = pd.Categorical(df_plot['age_group'], categories=age_group_order, ordered=True)
sns.boxplot(data=df_plot, x='age_group', y='total_price', ax=axes[1], palette='Set2')
axes[1].set_title('Spending Distribution by Age Group')
axes[1].set_xlabel('Age Group')
axes[1].set_ylabel('Total Price (₹)')

plt.tight_layout()
plt.savefig('visualizations/03_age_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 3 saved: Age Analysis")

# ============================================================
# CHART 4: Region-wise Performance
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# revenue by region (pie chart)
region_revenue = df.groupby('region')['total_price'].sum()
colors_pie = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
explode = [0.05] * len(region_revenue)
axes[0].pie(region_revenue, labels=region_revenue.index, autopct='%1.1f%%', 
            colors=colors_pie, explode=explode, shadow=True, startangle=140)
axes[0].set_title('Revenue Distribution by Region')

# avg order value by region
avg_order = df.groupby('region')['total_price'].mean().sort_values(ascending=True)
avg_order.plot(kind='barh', ax=axes[1], color='#26A69A')
axes[1].set_title('Average Order Value by Region')
axes[1].set_xlabel('Avg Order Value (₹)')
axes[1].set_ylabel('')

plt.tight_layout()
plt.savefig('visualizations/04_region_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 4 saved: Region Analysis")

# ============================================================
# CHART 5: Payment Method Analysis
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# payment method distribution
payment_counts = df['payment_method'].value_counts()
colors_bar = sns.color_palette("coolwarm", len(payment_counts))
payment_counts.plot(kind='bar', ax=axes[0], color=colors_bar)
axes[0].set_title('Orders by Payment Method')
axes[0].set_xlabel('Payment Method')
axes[0].set_ylabel('Number of Orders')
axes[0].tick_params(axis='x', rotation=45)

# avg spending by payment method
avg_spending = df.groupby('payment_method')['total_price'].mean().sort_values(ascending=False)
avg_spending.plot(kind='bar', ax=axes[1], color=sns.color_palette("rocket", len(avg_spending)))
axes[1].set_title('Avg Spending by Payment Method')
axes[1].set_xlabel('Payment Method')
axes[1].set_ylabel('Avg Total Price (₹)')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('visualizations/05_payment_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 5 saved: Payment Analysis")

# ============================================================
# CHART 6: Correlation Heatmap
# ============================================================

fig, ax = plt.subplots(figsize=(10, 8))

numeric_cols = ['customer_age', 'quantity', 'unit_price', 'discount_pct', 'total_price', 'rating']
corr_matrix = df[numeric_cols].corr()

mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdYlBu_r', center=0,
            fmt='.2f', linewidths=1, ax=ax, square=True,
            cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Heatmap of Numerical Features')

plt.tight_layout()
plt.savefig('visualizations/06_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 6 saved: Correlation Heatmap")

# ============================================================
# CHART 7: Top 10 Customers by Spending
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

top_customers = df.groupby('customer_id')['total_price'].sum().nlargest(10).sort_values()
colors_top = sns.color_palette("YlOrRd", len(top_customers))
top_customers.plot(kind='barh', ax=ax, color=colors_top)
ax.set_title('Top 10 Customers by Total Spending')
ax.set_xlabel('Total Spending (₹)')
ax.set_ylabel('Customer ID')

# add value labels
for i, v in enumerate(top_customers.values):
    ax.text(v + 200, i, f'₹{v:,.0f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('visualizations/07_top_customers.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 7 saved: Top Customers")

# ============================================================
# CHART 8: Discount Impact on Sales
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# discount category distribution
discount_counts = df['discount_category'].value_counts()
discount_counts.plot(kind='pie', ax=axes[0], autopct='%1.1f%%', 
                     colors=['#66BB6A', '#FFA726', '#EF5350', '#AB47BC'],
                     startangle=90)
axes[0].set_title('Order Distribution by Discount Level')
axes[0].set_ylabel('')

# avg rating vs discount
discount_rating = df.groupby('discount_category')['rating'].mean()
discount_order = ['No Discount', 'Low', 'Medium', 'High']
discount_rating = discount_rating.reindex(discount_order)
bars = axes[1].bar(discount_rating.index, discount_rating.values, 
                   color=['#66BB6A', '#FFA726', '#EF5350', '#AB47BC'])
axes[1].set_title('Average Rating by Discount Level')
axes[1].set_xlabel('Discount Level')
axes[1].set_ylabel('Average Rating')
axes[1].set_ylim(0, 5)

# add value labels on bars
for bar, val in zip(bars, discount_rating.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f'{val:.2f}', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('visualizations/08_discount_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 8 saved: Discount Analysis")

# ============================================================
# CHART 9: Gender-wise Analysis
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# gender distribution
gender_counts = df['gender'].value_counts()
gender_counts.plot(kind='bar', ax=axes[0], color=['#42A5F5', '#EF5350', '#66BB6A'])
axes[0].set_title('Customer Gender Distribution')
axes[0].set_xlabel('Gender')
axes[0].set_ylabel('Count')
axes[0].tick_params(axis='x', rotation=0)

# gender vs category heatmap
gender_category = pd.crosstab(df['gender'], df['product_category'])
sns.heatmap(gender_category, annot=True, fmt='d', cmap='YlGnBu', ax=axes[1])
axes[1].set_title('Gender vs Product Category (Order Count)')
axes[1].set_xlabel('Product Category')
axes[1].set_ylabel('Gender')

plt.tight_layout()
plt.savefig('visualizations/09_gender_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 9 saved: Gender Analysis")

# ============================================================
# CHART 10: Year-over-Year Comparison
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

yearly_monthly = df.groupby(['order_year', 'order_month'])['total_price'].sum().unstack(level=0)
yearly_monthly.plot(kind='bar', ax=ax, width=0.8, color=['#5C6BC0', '#FF7043'])
ax.set_title('Year-over-Year Monthly Revenue Comparison')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue (₹)')
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
ax.legend(title='Year')

plt.tight_layout()
plt.savefig('visualizations/10_yoy_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 10 saved: Year-over-Year Comparison")

print("\n" + "=" * 60)
print("All visualizations saved in 'visualizations/' folder!")
print("=" * 60)
