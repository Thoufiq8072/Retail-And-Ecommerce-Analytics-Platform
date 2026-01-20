# Sample Data Overview

This directory contains **sample extracts** from each layer of the data pipeline
(Bronze, Silver, and Gold).  
Each sample file is intentionally limited to **5 rows** per table to make the
project easy to review without requiring Databricks access.

---
## 📁 Directory Structure

```

data/
├── raw/kaggle/global_fashion → Original source CSV files (Kaggle dataset)
├── bronze/ → Raw ingested data with metadata
├── silver/ → Cleaned and standardized data
├── gold/ → Analytics-ready dimensional tables


```
---
## Source Data Samples

Source samples represent **raw data**.


Example files:
- `customers_sample.csv`
- `products_sample.csv`
- `transactions_sample.csv`

---

## 🥉 Bronze Samples

Bronze samples represent **raw ingested data** with minimal transformation.

- Schema applied
- No business logic
- Ingestion metadata included

Example files:
- `bronze_customers_sample.csv`
- `bronze_products_sample.csv`
- `bronze_transactions_sample.csv`

---

## 🥈 Silver Samples

Silver samples contain **cleaned and standardized data**.

- Deduplicated records
- Normalized column names
- Validated business keys

Example files:
- `silver_customers_sample.csv`
- `silver_products_sample.csv`
- `silver_transactions_sample.csv`

---

## 🥇 Gold Samples

Gold samples represent the **final dimensional model** used for analytics.

- Star schema design
- Surrogate keys
- Fact and dimension tables separated

Example files:
- `dim_customers_sample.csv`
- `dim_products_sample.csv`
- `fact_sales_sample.csv`
- `fact_returns_sample.csv`

---

## ℹ️ Notes

- Each sample file contains **only 5 rows**
- Full datasets are processed in Databricks and stored as Delta tables
- Sample data is provided for **documentation, validation, and review purposes only**