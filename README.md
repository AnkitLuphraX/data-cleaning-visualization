# Data Cleaning & Visualization Project

A data analysis project that demonstrates end-to-end data preprocessing, cleaning, and visual storytelling using Python.

## 📌 About

This project works with a simulated e-commerce sales dataset containing **1500+ records** with various data quality issues (missing values, duplicates, outliers, and inconsistent formatting). The goal is to clean the data systematically and then create meaningful visualizations to uncover business insights.

## 🛠️ Tech Stack

- **Python 3.x**
- **Pandas** – data manipulation and cleaning
- **NumPy** – numerical operations
- **Matplotlib** – static visualizations
- **Seaborn** – statistical charts and heatmaps

## 📁 Project Structure

```
├── generate_dataset.py          # generates the raw dataset with dirty data
├── data_cleaning.py             # step-by-step data cleaning pipeline
├── data_visualization.py        # creates 10 individual chart types
├── dashboard_report.py          # generates a combined dashboard + prints insights
├── ecommerce_sales_raw.csv      # raw dataset (generated)
├── ecommerce_sales_cleaned.csv  # cleaned dataset (output)
├── visualizations/              # all saved charts and dashboard
│   ├── 01_category_analysis.png
│   ├── 02_monthly_trend.png
│   ├── 03_age_analysis.png
│   ├── ...
│   └── dashboard_report.png
├── requirements.txt
└── README.md
```

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/data-cleaning-visualization.git
   cd data-cleaning-visualization
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the raw dataset**
   ```bash
   python generate_dataset.py
   ```

4. **Run data cleaning**
   ```bash
   python data_cleaning.py
   ```

5. **Create visualizations**
   ```bash
   python data_visualization.py
   ```

6. **Generate the dashboard report**
   ```bash
   python dashboard_report.py
   ```

## 📊 Key Features

### Data Cleaning
- Identified and handled **80+ missing values** across 5 columns
- Removed **30 duplicate** records using order ID matching
- Standardized inconsistent categorical values (e.g., gender formatting)
- Detected and treated **12 outliers** using IQR method
- Fixed **5 negative quantity** errors (data entry mistakes)
- Created derived features: age groups, discount categories, time-based fields

### Visualizations Created
| # | Chart | Description |
|---|-------|-------------|
| 1 | Category Analysis | Revenue and order count by product category |
| 2 | Monthly Trend | Revenue trend over 24 months with area fill |
| 3 | Age Analysis | Customer age distribution and spending patterns |
| 4 | Region Analysis | Geographic revenue distribution (pie + bar) |
| 5 | Payment Analysis | Payment method preferences and avg spending |
| 6 | Correlation Heatmap | Relationships between numerical features |
| 7 | Top Customers | Highest spending customers |
| 8 | Discount Analysis | Impact of discounts on orders and ratings |
| 9 | Gender Analysis | Gender distribution and category preferences |
| 10 | YoY Comparison | Year-over-year monthly revenue comparison |

### Dashboard
A combined 6-panel dashboard image summarizing all key metrics at a glance.

## 💡 Key Insights

- Electronics and Home & Kitchen categories generate the highest revenue
- UPI and Credit Card are the most popular payment methods
- Customer ratings remain consistent regardless of discount levels
- The 26-35 age group represents the highest spending segment
- Sales show a relatively stable pattern across both years

## 📝 What I Learned

- How to systematically approach data quality issues
- Different strategies for handling missing data (mean, median, mode)
- Using IQR method to detect and treat outliers
- Creating professional-grade visualizations with Matplotlib and Seaborn
- Building a multi-chart dashboard for data storytelling
- Feature engineering to extract more value from existing data

## 📄 License

This project is for educational purposes as part of my internship coursework.
