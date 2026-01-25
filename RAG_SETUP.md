# RAG System Setup Guide

## Overview
This guide explains how to set up and use the Retrieval-Augmented Generation (RAG) system for your Retail Analytics Platform using Google Gemini.

## Architecture

```
┌─────────────────────────────┐
│   User Query (Natural Lang) │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  RAG Service                │
│  - Context Retrieval        │
│  - Data Aggregation         │
└──────────────┬──────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌─────▼──────────┐
│ Databricks  │  │ Google Gemini  │
│ Gold Tables │  │ (2.0-Flash)    │
└─────────────┘  └────────────────┘
```

## Prerequisites

1. **Google Gemini API Key**
   - Visit: https://ai.google.dev/
   - Sign up and generate an API key
   - Keep it secure (don't commit to git)

2. **Databricks Environment**
   - Access to your retail analytics workspace
   - Gold layer tables created and populated
   - Spark cluster running

3. **Python Environment**
   - Python 3.8+
   - Required packages (see Installation)

## Installation

### 1. Install Required Packages

```bash
pip install -r src/requirements_rag.txt
```

Or manually install:
```bash
pip install google-generativeai pyspark pandas python-dotenv
```

### 2. Configure API Key

**Option A: Environment Variable (Recommended)**

```bash
# Create .env file
cp .env.example .env
# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_api_key_here
```

Then load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```

**Option B: Direct Configuration**

```python
from src.rag_service import RetailAnalyticsRAG

rag = RetailAnalyticsRAG(gemini_api_key='your-api-key-here')
```

**Option C: Interactive Prompt**

```python
import getpass
api_key = getpass.getpass("Enter your Gemini API key: ")
```

## Usage

### Basic Query

```python
from src.rag_service import RetailAnalyticsRAG

# Initialize
rag = RetailAnalyticsRAG()

# Ask a question
response = rag.query("What is our total sales revenue?")
print(response)
```

### SQL-Enhanced Queries

```python
sql_query = """
SELECT 
  category,
  SUM(line_total) as revenue,
  COUNT(*) as transactions
FROM retail_analytics.gold.fact_sales fs
JOIN retail_analytics.gold.dim_products dp ON fs.product_sk = dp.product_sk
GROUP BY category
ORDER BY revenue DESC
"""

response = rag.query_with_sql(
    "Analyze our sales by product category",
    sql_query
)
print(response)
```

### Interactive Multi-Turn Conversation

```python
rag = RetailAnalyticsRAG()
rag.multi_turn_conversation()

# In the interactive session, ask questions like:
# "What's our total revenue?"
# "Who are our top customers?"
# "Which products sell best?"
# Type 'exit' to quit
```

## Available Query Types

### 1. Automatic Context Retrieval
The system automatically fetches relevant data based on query keywords:

- **Sales queries**: "sales", "revenue", "transaction", "invoice", "sold"
- **Customer queries**: "customer", "client", "buyer", "order"
- **Product queries**: "product", "item", "category"

```python
# The system intelligently retrieves context
response = rag.query("What are our top-selling products?")
```

### 2. Custom SQL Queries
For specific, complex analyses:

```python
sql = "SELECT ... FROM retail_analytics.gold.* WHERE ..."
response = rag.query_with_sql(question, sql)
```

### 3. Summary Analytics
Quick access to key metrics:

```python
response = rag.query("Give me a summary of our business")
```

## Available Gold Tables

### Fact Tables
- **fact_sales**: Transaction-level sales data
  - Columns: sales_sk, date_sk, customer_sk, product_sk, store_sk, employee_sk, discount_sk, invoice_id, line, size, unit_price, quantity, line_total, invoice_total

- **fact_returns**: Return/refund transactions
  - Columns: return_sk, date_sk, customer_sk, product_sk, store_sk, return_reason, refund_amount, return_date

### Dimension Tables
- **dim_customers**: Customer master data
- **dim_products**: Product master data with multilingual descriptions
- **dim_stores**: Store locations and information
- **dim_employees**: Employee records
- **dim_dates**: Date dimension with calendar information
- **dim_discounts**: Discount and promotion data

## Example Queries

### Sales Analysis
```python
rag.query("What was our revenue in Q3? How many transactions did we have?")
rag.query("Show me sales trends by month")
```

### Customer Analysis
```python
rag.query("Who are our top 10 customers?")
rag.query("What's the customer distribution by country?")
rag.query("Analyze customer spending patterns")
```

### Product Analysis
```python
rag.query("Which product categories perform best?")
rag.query("Show me products with high and low sales")
rag.query("Analyze pricing strategy by category")
```

### Store Performance
```python
rag.query("Which stores have the highest revenue?")
rag.query("Compare store performance across regions")
rag.query("Show employee count vs sales by store")
```

## Notebook Usage

Launch the Jupyter notebook with RAG demos:

```bash
# In Databricks
# Navigate to: notebooks/05_rag/rag_demo.ipynb

# Or locally
jupyter notebook notebooks/05_rag/rag_demo.ipynb
```

The notebook includes:
1. Setup and configuration
2. Data overview
3. Example queries
4. SQL-enhanced queries
5. Interactive mode
6. Advanced analyses

## Performance Considerations

1. **Data Retrieval**
   - Queries retrieve up to 100 rows by default
   - Adjust `limit` parameter in query_params for larger datasets
   - Consider filtering by date range for large tables

2. **API Costs**
   - Gemini API charges per request
   - Retrieved data is included in prompt, which affects token count
   - Monitor API usage in Google Cloud Console

3. **Response Time**
   - Initial context retrieval: 1-5 seconds
   - API response generation: 2-10 seconds
   - Total query time: 3-15 seconds

## Troubleshooting

### Issue: "GEMINI_API_KEY not provided"
**Solution**: Set the API key via environment variable or parameter
```python
rag = RetailAnalyticsRAG(gemini_api_key='your-key')
```

### Issue: "Table not found" errors
**Solution**: Ensure Spark cluster is running and tables exist
```python
spark.sql("SELECT * FROM retail_analytics.gold.fact_sales LIMIT 1").show()
```

### Issue: Poor response quality
**Solution**: 
- Provide more specific context in your question
- Use SQL-enhanced queries for precise data
- Adjust temperature parameter in generation_config (default: 0.7)

### Issue: High API costs
**Solution**:
- Limit data retrieval with smaller `limit` values
- Use SQL filtering to reduce context size
- Cache frequently used queries

## Advanced Configuration

### Custom System Prompt
Edit the `system_prompt` variable in `rag_service.py` to customize RAG behavior.

### Temperature and Generation Parameters
Adjust in the `generate_content()` call:

```python
generation_config=genai.types.GenerationConfig(
    temperature=0.7,  # 0.0-1.0 (higher = more creative)
    top_p=0.95,       # Nucleus sampling
    max_output_tokens=2048  # Maximum response length
)
```

### Custom Table Schemas
Update `self.table_schemas` dictionary to include new tables or columns.

## Security Best Practices

1. **Never commit API keys**
   - Use `.env` file with `.gitignore`
   - Use environment variables in production
   - Rotate keys regularly

2. **Data Privacy**
   - Be aware of sensitive data in gold tables
   - Implement access controls if needed
   - Consider data minimization in prompts

3. **API Rate Limiting**
   - Monitor request frequency
   - Implement caching for common queries
   - Use batch processing for bulk analyses

## Integration with CI/CD

For production deployments:

```yaml
# Example: GitHub Actions
env:
  GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
```

Or in Databricks:
```python
# Use Databricks secrets
api_key = dbutils.secrets.get(scope="gemini", key="api_key")
```

## Next Steps

1. ✅ Set up Gemini API key
2. ✅ Install required packages
3. ✅ Configure environment variables
4. ✅ Run `rag_demo.ipynb` notebook
5. ✅ Experiment with custom queries
6. ✅ Integrate into your data applications

## Support and Resources

- [Google Gemini Documentation](https://ai.google.dev/docs)
- [Databricks Python API](https://docs.databricks.com/dev-tools/python/index.html)
- [RAG Best Practices](https://ai.google.dev/docs/concepts)

## Contributing

To improve the RAG system:
1. Add new retrieval methods in `rag_service.py`
2. Create example queries in `rag_demo.ipynb`
3. Submit improvements via pull requests

---

**Last Updated**: January 2026
**RAG System Version**: 1.0
**Gemini API**: 2.0-Flash
