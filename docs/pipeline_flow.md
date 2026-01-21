# Data Pipeline Flow

This document explains the end-to-end data movement in the platform.

---

## step 1 : Environment Setup
- Run all the files inside `src/`
- Create **catalog, schema and volumes**. run `notebooks/00_setup/env_setup`
- Get **Kaggle API Key**

```

kaggle Login -> profile -> settings -> API Tokens -> Generate New Token


```
- Store API-key and Username in `.env` file
- Create connection between kaggle and Databricks. run `notebooks/00_setup/kaggle_auth`

---

## Step 2: Ingestion
- Run `notebooks/01_ingestion/data_ingestion`
- CSV files will be downloaded from Kaggle using Kaggle API
- Stored under the volume `/Volumes/retail_analytics/raw/kaggle/global_fashion/`

---

## Step 3: Bronze Processing
- Read raw CSVs
- Add ingestion timestamps
- Write to Delta format
- **Run** `notebooks/02_bronze/`

---

## Step 4: Silver Processing
- Clean invalid records
- Standardize column names
- Apply business rules
- Remove duplicates
- **Run** `notebooks/03_silver/`

---

## Step 5: Gold Processing
- First create Dimension Tables then Fact Tables
- Build dimension tables
- Generate surrogate keys
- Build fact tables
- Enforce analytical grain
- **Run** the files in the below order
```

notebooks/04_gold/dim_dates
notebooks/04_gold/dim_customers
notebooks/04_gold/dim_discounts
notebooks/04_gold/dim_products
notebooks/04_gold/dim_employees
notebooks/04_gold/dim_stores
notebooks/04_gold/fact_sales
notebooks/04_gold/fact_returns


```
---

## Step 6: Consumption
- Databricks SQL queries
- Dashboard visualizations
- **Run** the file `notebooks/04_gold/gold_views`
- Click `sql/dashboard/Retail-Analytics-Dashboard.lvdash.json` it will automatically redirect you to SQL Dashboard Page
- Refer `sql/visualizations/` for sample visuals
- Refer `sql/dashboard/README.md` to know about the used KPI metrics in SQL Dashboard