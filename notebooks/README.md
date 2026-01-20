# Databricks Workspace Guide

This document explains how this project is structured and executed inside
a Databricks workspace.

The project follows a **layered notebook design**, where each notebook
represents a logical stage of the data pipeline.

---

## 🗂 Workspace Structure

```

notebooks/
├── 00_setup → Environment & authentication setup
├── 01_ingestion → Raw data ingestion
├── 02_bronze → Bronze layer processing
├── 03_silver → Silver layer transformations
├── 04_gold → Gold layer dimensional modeling


```
---

## ▶ Execution Order

Notebooks should be executed in the following order:

1. `00_setup/env_setup.ipynb`
2. `00_setup/kaggle_auth.ipynb`
3. `01_ingestion/data_ingestion.ipynb`
4. `02_bronze/*`
5. `03_silver/*`
6. `04_gold/*`

Each stage depends on the successful completion of the previous layer.

---

## ⚙️ Environment Setup

- Python modules under `/src` are imported into notebooks
- Environment variables are loaded from `.env`
- Delta Lake is used for all persisted tables

---

## 🧠 Design Principles

- Notebooks handle orchestration, not reusable logic
- Reusable code lives in `/src`
- Each layer is idempotent and re-runnable
- No dashboards directly query Bronze or Silver layers

---

## 📊 Analytics & Dashboards

- Gold tables are exposed through Databricks SQL
- Dashboards are defined under `sql/dashboard/`
- All business metrics are derived from Gold layer tables only

---

## ℹ️ Notes

- Sample CSVs under `/data` are for GitHub visibility only
- Full-scale processing happens inside Databricks using Delta tables