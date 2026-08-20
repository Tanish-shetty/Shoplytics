# E-Commerce Sales & Customer Analytics Dashboard

This repository contains an end-to-end analytics portfolio project built from the public Kaggle dataset `maramsa/e-commerce-sales-and-customer-analytics-dataset`. The workflow covers raw data ingestion, cleaning and enrichment, exploratory analysis, SQL analytics, customer segmentation, business insight generation, and a custom frontend analytics dashboard.

## Overview

The project answers practical e-commerce questions around revenue, profitability, category performance, regional performance, customer value, repeat purchase behavior, and retention risk. The source dataset is relatively minimal, so the Python pipeline adds reproducible business fields such as sub-category, geographic detail, discounts, shipping cost, payment method, and product cost price to support a more complete analytics model.

## Business Questions

- How much revenue and profit is the business generating?
- How does sales performance change month over month?
- Which categories, products, and regions drive the most revenue?
- Which categories and products are strongest on profit margin?
- Which customers are most valuable?
- What share of customers are repeat buyers?
- Which customer segments are at risk of inactivity?
- Which actions would improve growth and profitability?

## Dataset

Source: Kaggle dataset `maramsa/e-commerce-sales-and-customer-analytics-dataset`

Raw tables:

- `customers.csv`
- `orders.csv`
- `order_items.csv`
- `products.csv`

Processed outputs:

- `data/processed/customers_clean.csv`
- `data/processed/products_clean.csv`
- `data/processed/orders_clean.csv`
- `data/processed/date_dim.csv`
- `data/processed/customer_segments.csv`
- `data/processed/customer_segment_summary.csv`
- `data/processed/project_summary.csv`
- `frontend/data/dashboard_data.json`

## Tech Stack

```text
Python
Pandas
NumPy
SQL
PostgreSQL
SQLite
Matplotlib
Seaborn
Jupyter
HTML/CSS/JavaScript
```

## Project Architecture

```text
Raw Data
  ->
Python Data Cleaning + Enrichment
  ->
Processed Data
  ->
PostgreSQL / SQLite Validation
  ->
SQL Analytics
  ->
Frontend Dashboard
  ->
Business Insights
```

## Features

- Python cleaning pipeline that standardizes and enriches customer, product, and order data
- RFM-based customer segmentation with explainable segment labels
- SQL analysis scripts for KPIs, sales, customers, products, regions, and advanced trends
- Executed EDA notebook plus exported charts for portfolio presentation
- Interactive frontend dashboard with filters for status, region, category, and payment method
- Business insight report backed by actual calculations from the processed dataset

## Key Metrics

- Total Revenue: `284,741.58`
- Total Profit: `53,643.61`
- Total Orders: `695`
- Total Customers: `267`
- Total Units Sold: `4,848`
- Average Order Value: `409.70`
- Profit Margin: `18.84%`
- Repeat Customer Rate: `73.41%`

## Key Insights

- `Hair` is the largest revenue category, but `Body` is the most profitable by margin.
- `Southern Europe` is the strongest region by both revenue and order volume.
- Repeat customers drive `89.62%` of revenue, making retention a major lever.
- `Champions` contribute the largest share of segment revenue, while `At Risk` customers still represent significant revenue exposure.
- Several high-revenue products show weaker margins and deserve pricing or discount review.

## Project Structure

```text
Shoplytics/
|-- data/
|   |-- raw/
|   |   |-- customers.csv
|   |   |-- orders.csv
|   |   |-- order_items.csv
|   |   `-- products.csv
|   `-- processed/
|       |-- customers_clean.csv
|       |-- products_clean.csv
|       |-- orders_clean.csv
|       |-- date_dim.csv
|       |-- customer_segments.csv
|       |-- customer_segment_summary.csv
|       |-- project_summary.csv
|       `-- shoplytics_validation.sqlite
|-- frontend/
|   |-- data/
|   |   `-- dashboard_data.json
|   |-- app.js
|   |-- index.html
|   `-- styles.css
|-- notebooks/
|   `-- ecommerce_eda.ipynb
|-- python/
|   |-- build_dashboard_data.py
|   |-- data_cleaning.py
|   |-- customer_segmentation.py
|   `-- eda.py
|-- reports/
|   |-- business_insights.md
|   `-- figures/
|-- sql/
|   |-- schema.sql
|   |-- data_quality.sql
|   |-- kpi_analysis.sql
|   |-- sales_analysis.sql
|   |-- customer_analysis.sql
|   |-- product_analysis.sql
|   |-- regional_analysis.sql
|   `-- advanced_analysis.sql
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## How to Run

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Optional: download the Kaggle dataset yourself and point the pipeline to it:

```python
import kagglehub
path = kagglehub.dataset_download("maramsa/e-commerce-sales-and-customer-analytics-dataset")
print(path)
```

4. Set the dataset path only if you want to override the default cached location:

```powershell
$env:KAGGLE_DATASET_PATH="C:\real\path\to\dataset"
```

5. Run the project pipeline:

```powershell
python python/data_cleaning.py
python python/customer_segmentation.py
python python/eda.py
python python/build_dashboard_data.py
jupyter nbconvert --to notebook --execute .\notebooks\ecommerce_eda.ipynb --inplace
```

6. Launch the frontend dashboard:

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000/frontend/` in your browser.

If PowerShell blocks script activation on your machine, run the project directly with the virtual environment interpreter:

```powershell
.\.venv\Scripts\python python\data_cleaning.py
.\.venv\Scripts\python python\customer_segmentation.py
.\.venv\Scripts\python python\eda.py
.\.venv\Scripts\python python\build_dashboard_data.py
.\.venv\Scripts\python -m http.server 8000
```

## SQL Notes

- `sql/schema.sql` is written for PostgreSQL-style modeling.
- The project was locally validated with `data/processed/shoplytics_validation.sqlite` because PostgreSQL was not available in this environment.
- KPI definitions are consistent across Python, SQL, and the frontend dashboard: only `Completed` orders contribute recognized revenue.

## Frontend Dashboard

The frontend dashboard lives in [`frontend/index.html`](frontend/index.html) and reads from `frontend/data/dashboard_data.json`, which is generated by [`python/build_dashboard_data.py`](python/build_dashboard_data.py).

It includes:

- KPI cards for revenue, profit, customers, and AOV
- Filter controls for status, region, category, and payment method
- Monthly trend, category mix, regional performance, and segment views
- Product leaderboards and a high-revenue / low-margin watchlist

## Resume-Ready Outcome

This project supports resume bullets such as:

- Analyzed e-commerce sales and customer data using Python, SQL, and a custom frontend dashboard to identify revenue, profitability, product, and regional performance trends.
- Built KPI logic for revenue, profit margin, AOV, repeat customer rate, and customer segmentation.
- Performed RFM-based segmentation to identify champions, loyal customers, and at-risk customers for retention strategy.
