# generate_dataset.py
# Quick script to create a sample e-commerce sales dataset
# Run this once to generate the CSV file used in the analysis

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# --- config ---
num_records = 1500
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys']
regions = ['North', 'South', 'East', 'West', 'Central']
payment_methods = ['Credit Card', 'UPI', 'Debit Card', 'Cash on Delivery', 'Net Banking']

# generate base data
data = {
    'order_id': [f'ORD-{i+1001}' for i in range(num_records)],
    'order_date': [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(num_records)],
    'customer_id': [f'CUST-{random.randint(100, 600)}' for _ in range(num_records)],
    'customer_age': [random.randint(18, 65) for _ in range(num_records)],
    'gender': [random.choice(['Male', 'Female', 'Other']) for _ in range(num_records)],
    'product_category': [random.choice(categories) for _ in range(num_records)],
    'quantity': [random.randint(1, 10) for _ in range(num_records)],
    'unit_price': [round(random.uniform(99, 4999), 2) for _ in range(num_records)],
    'discount_pct': [random.choice([0, 5, 10, 15, 20, 25, 30]) for _ in range(num_records)],
    'region': [random.choice(regions) for _ in range(num_records)],
    'payment_method': [random.choice(payment_methods) for _ in range(num_records)],
    'rating': [round(random.uniform(1.0, 5.0), 1) for _ in range(num_records)],
}

df = pd.DataFrame(data)

# calculate total price
df['total_price'] = round(df['quantity'] * df['unit_price'] * (1 - df['discount_pct']/100), 2)

# --- introduce some "dirty" data to make cleaning interesting ---

# 1) add missing values randomly
missing_indices = np.random.choice(df.index, size=80, replace=False)
df.loc[missing_indices[:25], 'customer_age'] = np.nan
df.loc[missing_indices[25:45], 'gender'] = np.nan
df.loc[missing_indices[45:60], 'rating'] = np.nan
df.loc[missing_indices[60:75], 'payment_method'] = np.nan
df.loc[missing_indices[75:], 'discount_pct'] = np.nan

# 2) add some duplicates
duplicate_rows = df.sample(n=30, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# 3) add outliers in unit_price (some unrealistically high values)
outlier_indices = np.random.choice(df.index, size=12, replace=False)
df.loc[outlier_indices, 'unit_price'] = np.random.uniform(15000, 50000, size=12).round(2)

# 4) add some negative quantities (data entry errors)
neg_indices = np.random.choice(df.index, size=5, replace=False)
df.loc[neg_indices, 'quantity'] = -1 * df.loc[neg_indices, 'quantity']

# 5) add inconsistent gender values
df.loc[df.index[100], 'gender'] = 'male'   # lowercase
df.loc[df.index[200], 'gender'] = 'FEMALE'  # uppercase
df.loc[df.index[300], 'gender'] = 'f'
df.loc[df.index[400], 'gender'] = 'M'

# shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# save to csv
df.to_csv('ecommerce_sales_raw.csv', index=False)
print(f"Dataset generated successfully! Shape: {df.shape}")
print(f"Saved as 'ecommerce_sales_raw.csv'")
print(f"\nQuick preview:")
print(df.head())
