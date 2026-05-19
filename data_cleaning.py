"""
Data Cleaning Script - E-commerce Sales Dataset
=================================================
Author: Ankit
Date: May 2026

This script performs data cleaning on the raw e-commerce sales dataset.
Steps covered:
  1. Loading and initial exploration
  2. Handling missing values
  3. Removing duplicates
  4. Fixing data inconsistencies
  5. Treating outliers
  6. Feature engineering
  7. Saving the cleaned dataset
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# STEP 1: Load the dataset and do initial exploration
# ============================================================

print("=" * 60)
print("STEP 1: Loading and Exploring the Dataset")
print("=" * 60)

df = pd.read_csv('ecommerce_sales_raw.csv')

print(f"\nDataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"\nColumn Names:\n{list(df.columns)}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nFirst 5 rows:")
print(df.head())

# checking basic stats
print(f"\n--- Basic Statistics ---")
print(df.describe())

# ============================================================
# STEP 2: Handle Missing Values
# ============================================================

print("\n" + "=" * 60)
print("STEP 2: Handling Missing Values")
print("=" * 60)

# first lets see how many missing values are there
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_info = pd.DataFrame({'Missing Count': missing, 'Percentage': missing_pct})
missing_info = missing_info[missing_info['Missing Count'] > 0]
print(f"\nMissing Values Summary:")
print(missing_info)

# Handle customer_age - fill with median (since age can have outliers, median is better than mean)
median_age = df['customer_age'].median()
df['customer_age'] = df['customer_age'].fillna(median_age)
print(f"\n-> Filled missing customer_age with median: {median_age}")

# Handle gender - fill with mode (most common value)
mode_gender = df['gender'].mode()[0]
df['gender'] = df['gender'].fillna(mode_gender)
print(f"-> Filled missing gender with mode: {mode_gender}")

# Handle rating - fill with mean rating
mean_rating = round(df['rating'].mean(), 1)
df['rating'] = df['rating'].fillna(mean_rating)
print(f"-> Filled missing rating with mean: {mean_rating}")

# Handle payment_method - fill with mode
mode_payment = df['payment_method'].mode()[0]
df['payment_method'] = df['payment_method'].fillna(mode_payment)
print(f"-> Filled missing payment_method with mode: {mode_payment}")

# Handle discount_pct - fill with 0 (assuming no discount if not specified)
df['discount_pct'] = df['discount_pct'].fillna(0)
print("-> Filled missing discount_pct with 0 (no discount)")

# verify no more missing values
print(f"\nRemaining missing values: {df.isnull().sum().sum()}")

# ============================================================
# STEP 3: Remove Duplicates
# ============================================================

print("\n" + "=" * 60)
print("STEP 3: Removing Duplicates")
print("=" * 60)

initial_rows = len(df)
# checking duplicates based on order_id (each order should be unique)
duplicates = df[df.duplicated(subset=['order_id'], keep='first')]
print(f"\nDuplicate orders found: {len(duplicates)}")

df = df.drop_duplicates(subset=['order_id'], keep='first')
print(f"Rows before: {initial_rows} -> Rows after: {len(df)}")
print(f"Removed {initial_rows - len(df)} duplicate rows")

# ============================================================
# STEP 4: Fix Data Inconsistencies
# ============================================================

print("\n" + "=" * 60)
print("STEP 4: Fixing Data Inconsistencies")
print("=" * 60)

# Check unique gender values - there might be inconsistent formatting
print(f"\nUnique gender values before cleaning: {df['gender'].unique()}")

# standardize gender values
gender_mapping = {
    'Male': 'Male', 'male': 'Male', 'M': 'Male', 'm': 'Male',
    'Female': 'Female', 'female': 'Female', 'FEMALE': 'Female', 'F': 'Female', 'f': 'Female',
    'Other': 'Other', 'other': 'Other'
}
df['gender'] = df['gender'].map(gender_mapping)

# fill any remaining unmapped genders
df['gender'] = df['gender'].fillna('Other')
print(f"Unique gender values after cleaning: {df['gender'].unique()}")

# convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'])
print(f"\nConverted order_date to datetime format")

# make sure customer_age is integer
df['customer_age'] = df['customer_age'].astype(int)

# ============================================================
# STEP 5: Handle Outliers
# ============================================================

print("\n" + "=" * 60)
print("STEP 5: Handling Outliers")
print("=" * 60)

# Fix negative quantities (data entry errors - take absolute value)
negative_qty = df[df['quantity'] < 0]
print(f"\nNegative quantities found: {len(negative_qty)}")
df['quantity'] = df['quantity'].abs()
print("-> Converted negative quantities to positive (absolute value)")

# Handle outliers in unit_price using IQR method
Q1 = df['unit_price'].quantile(0.25)
Q3 = df['unit_price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['unit_price'] < lower_bound) | (df['unit_price'] > upper_bound)]
print(f"\nUnit price outliers detected (IQR method): {len(outliers)}")
print(f"  Lower bound: {lower_bound:.2f}")
print(f"  Upper bound: {upper_bound:.2f}")

# cap outliers instead of removing them (to keep more data)
df['unit_price'] = df['unit_price'].clip(lower=lower_bound, upper=upper_bound)
print("-> Capped outliers using IQR bounds")

# ============================================================
# STEP 6: Feature Engineering
# ============================================================

print("\n" + "=" * 60)
print("STEP 6: Feature Engineering")
print("=" * 60)

# recalculate total_price after cleaning
df['total_price'] = round(df['quantity'] * df['unit_price'] * (1 - df['discount_pct']/100), 2)
print("-> Recalculated total_price after cleaning")

# extract month and year from order_date
df['order_month'] = df['order_date'].dt.month
df['order_year'] = df['order_date'].dt.year
df['month_name'] = df['order_date'].dt.strftime('%B')
print("-> Extracted order_month, order_year, and month_name")

# create age group bins
bins = [17, 25, 35, 45, 55, 66]
labels = ['18-25', '26-35', '36-45', '46-55', '56-65']
df['age_group'] = pd.cut(df['customer_age'], bins=bins, labels=labels)
print("-> Created age_group categories")

# create discount category
df['discount_category'] = pd.cut(df['discount_pct'], 
                                  bins=[-1, 0, 10, 20, 100],
                                  labels=['No Discount', 'Low', 'Medium', 'High'])
print("-> Created discount_category")

# ============================================================
# STEP 7: Final check and save
# ============================================================

print("\n" + "=" * 60)
print("STEP 7: Final Summary & Saving")
print("=" * 60)

print(f"\nCleaned Dataset Shape: {df.shape}")
print(f"Missing Values: {df.isnull().sum().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")

print(f"\nColumn Types:")
print(df.dtypes)

print(f"\nSample of cleaned data:")
print(df.head(10))

# save cleaned dataset
df.to_csv('ecommerce_sales_cleaned.csv', index=False)
print(f"\n[OK] Cleaned dataset saved as 'ecommerce_sales_cleaned.csv'")
print(f"   Final shape: {df.shape[0]} rows x {df.shape[1]} columns")
