# Source Utilities (`src/`)

This directory contains **reusable Python modules** used across Databricks
notebooks to avoid code duplication and improve maintainability.

All logic that is **environment-agnostic** and **not notebook-specific** is
placed here.

---

## 📁 Modules Overview

### `configs.py`
Centralized configuration values such as:
- Database names
- Table prefixes
- Environment-level constants

Purpose:
- Avoid hardcoded values inside notebooks
- Enable easier environment changes (dev / prod)

---

### `paths.py`
Defines standard paths used across the project:
- Raw data locations
- Bronze / Silver / Gold storage paths

Purpose:
- Single source of truth for file paths
- Prevent path inconsistencies across notebooks

---

### `schema_definitions.py`
Contains Spark schema definitions for:
- Silver layers
- Gold Layers

Purpose:
- Enforce schema consistency
- For Reference while writing

---

### `utils.py`
Shared utility functions such as:
- Common transformations
- Data validation helpers
- Reusable Spark logic

Purpose:
- Reduce repetitive notebook code
- Improve readability and testing potential

---

## 🧠 Design Philosophy

- Notebooks orchestrate **workflow**
- `src/` contains **reusable logic**
- Business logic lives in Silver & Gold notebooks
- No hardcoded paths or schemas in notebooks

---

## ℹ️ Notes

- These modules are imported into Databricks notebooks
- Designed for clarity and reusability, not for standalone execution
