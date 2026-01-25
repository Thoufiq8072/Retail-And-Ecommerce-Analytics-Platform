"""
RAG Service for Retail Analytics Platform
Connects to gold tables and uses Google Gemini for AI-powered insights
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import google.generativeai as genai
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from src.configs import CATALOG_NAME, GOLD_SCHEMA
from src.paths import (
    DIM_CUSTOMERS_PATH, DIM_PRODUCTS_PATH, DIM_STORES_PATH,
    DIM_DATES_PATH, DIM_EMPLOYEES_PATH, DIM_DISCOUNTS_PATH,
    FACT_SALES_PATH, FACT_RETURNS_PATH
)


class RetailAnalyticsRAG:
    """
    RAG system for Retail Analytics Platform using Google Gemini
    Retrieves data from gold tables and generates insights
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Initialize RAG service with Gemini API
        
        Args:
            gemini_api_key: Google Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        # Configure Gemini API
        api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not provided. Set it as parameter or environment variable."
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Initialize Spark
        self.spark = SparkSession.builder.appName("RetailAnalyticsRAG").getOrCreate()
        
        # Define table schemas for context
        self.table_schemas = {
            "fact_sales": [
                "sales_sk (PK)", "date_sk (FK)", "customer_sk (FK)", "product_sk (FK)",
                "store_sk (FK)", "employee_sk (FK)", "discount_sk (FK)", "invoice_id",
                "line", "size", "unit_price", "quantity", "line_total", "invoice_total"
            ],
            "fact_returns": [
                "return_sk (PK)", "date_sk (FK)", "customer_sk (FK)", "product_sk (FK)",
                "store_sk (FK)", "return_reason", "refund_amount", "return_date"
            ],
            "dim_customers": [
                "customer_sk (PK)", "customer_id", "name", "email", "telephone",
                "city", "country", "gender", "date_of_birth", "job_title",
                "_created_at", "_updated_at"
            ],
            "dim_products": [
                "product_sk (PK)", "product_id", "category", "sub_category", "color",
                "sizes", "production_cost", "description_pt", "description_de",
                "description_fr", "description_es", "description_en", "description_zh",
                "_created_at", "_updated_at"
            ],
            "dim_stores": [
                "store_sk (PK)", "store_id", "store_name", "city", "country",
                "zip_code", "latitude", "longitude", "number_of_employees",
                "_created_at", "_updated_at"
            ],
            "dim_employees": [
                "employee_sk (PK)", "employee_id", "store_id", "name", "position",
                "_created_at", "_updated_at"
            ],
            "dim_dates": [
                "date_sk (PK)", "date", "day", "month", "month_name", "quarter",
                "year", "day_of_week", "day_name", "is_weekend"
            ],
            "dim_discounts": [
                "discount_sk (PK)", "discount_start_date", "discount_end_date",
                "discount", "description", "category", "sub_category",
                "_created_at", "_updated_at"
            ]
        }
    
    def _retrieve_sales_data(self, query_params: Dict[str, Any]) -> str:
        """Retrieve sales data based on query parameters"""
        try:
            df = self.spark.table(FACT_SALES_PATH)
            
            # Apply filters
            if "customer_id" in query_params:
                customer_df = self.spark.table(DIM_CUSTOMERS_PATH).filter(
                    F.col("customer_id") == query_params["customer_id"]
                ).select("customer_sk").limit(1)
                customer_sk = customer_df.collect()[0][0] if customer_df.count() > 0 else None
                if customer_sk:
                    df = df.filter(F.col("customer_sk") == customer_sk)
            
            if "date_range" in query_params:
                start_date, end_date = query_params["date_range"]
                date_df = self.spark.table(DIM_DATES_PATH).filter(
                    (F.col("date") >= start_date) & (F.col("date") <= end_date)
                ).select("date_sk")
                date_sks = [row[0] for row in date_df.collect()]
                if date_sks:
                    df = df.filter(F.col("date_sk").isin(date_sks))
            
            if "store_id" in query_params:
                store_df = self.spark.table(DIM_STORES_PATH).filter(
                    F.col("store_id") == query_params["store_id"]
                ).select("store_sk").limit(1)
                store_sk = store_df.collect()[0][0] if store_df.count() > 0 else None
                if store_sk:
                    df = df.filter(F.col("store_sk") == store_sk)
            
            if "product_id" in query_params:
                product_df = self.spark.table(DIM_PRODUCTS_PATH).filter(
                    F.col("product_id") == query_params["product_id"]
                ).select("product_sk").limit(1)
                product_sk = product_df.collect()[0][0] if product_df.count() > 0 else None
                if product_sk:
                    df = df.filter(F.col("product_sk") == product_sk)
            
            # Limit results
            limit = query_params.get("limit", 100)
            result_json = df.limit(limit).toPandas().to_json(orient="records")
            return result_json
        except Exception as e:
            return f"Error retrieving sales data: {str(e)}"
    
    def _retrieve_customer_data(self, query_params: Dict[str, Any]) -> str:
        """Retrieve customer data"""
        try:
            df = self.spark.table(DIM_CUSTOMERS_PATH)
            
            if "customer_id" in query_params:
                df = df.filter(F.col("customer_id") == query_params["customer_id"])
            if "country" in query_params:
                df = df.filter(F.col("country") == query_params["country"])
            if "city" in query_params:
                df = df.filter(F.col("city") == query_params["city"])
            
            limit = query_params.get("limit", 50)
            result_json = df.limit(limit).toPandas().to_json(orient="records")
            return result_json
        except Exception as e:
            return f"Error retrieving customer data: {str(e)}"
    
    def _retrieve_product_data(self, query_params: Dict[str, Any]) -> str:
        """Retrieve product data"""
        try:
            df = self.spark.table(DIM_PRODUCTS_PATH)
            
            if "category" in query_params:
                df = df.filter(F.col("category") == query_params["category"])
            if "sub_category" in query_params:
                df = df.filter(F.col("sub_category") == query_params["sub_category"])
            
            limit = query_params.get("limit", 50)
            result_json = df.limit(limit).toPandas().to_json(orient="records")
            return result_json
        except Exception as e:
            return f"Error retrieving product data: {str(e)}"
    
    def _retrieve_analytics_summary(self) -> str:
        """Retrieve summary analytics from gold tables"""
        try:
            summaries = {}
            
            # Sales summary
            sales_df = self.spark.table(FACT_SALES_PATH)
            summaries["total_sales"] = sales_df.agg(
                F.sum("line_total").alias("total"),
                F.count("*").alias("transactions"),
                F.avg("line_total").alias("avg_transaction")
            ).collect()[0]
            
            # Customer summary
            customer_df = self.spark.table(DIM_CUSTOMERS_PATH)
            summaries["total_customers"] = customer_df.count()
            
            # Product summary
            product_df = self.spark.table(DIM_PRODUCTS_PATH)
            summaries["total_products"] = product_df.count()
            
            # Store summary
            store_df = self.spark.table(DIM_STORES_PATH)
            summaries["total_stores"] = store_df.count()
            
            return json.dumps({
                "total_sales_amount": float(summaries["total_sales"][0]),
                "total_transactions": int(summaries["total_sales"][1]),
                "avg_transaction_value": float(summaries["total_sales"][2]),
                "total_customers": summaries["total_customers"],
                "total_products": summaries["total_products"],
                "total_stores": summaries["total_stores"]
            })
        except Exception as e:
            return f"Error retrieving analytics summary: {str(e)}"
    
    def _create_retrieval_context(self, query: str) -> str:
        """
        Create context by retrieving relevant data based on the query
        Uses simple keyword matching to determine what data to retrieve
        """
        context_parts = []
        
        # Add table schema information
        context_parts.append("=== AVAILABLE TABLES SCHEMA ===\n")
        for table_name, columns in self.table_schemas.items():
            context_parts.append(f"\n{table_name}: {', '.join(columns)}")
        
        # Retrieve analytics summary
        context_parts.append("\n\n=== ANALYTICS SUMMARY ===")
        summary = self._retrieve_analytics_summary()
        context_parts.append(summary)
        
        # Smart retrieval based on query keywords
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["sales", "revenue", "transaction", "invoice", "sold"]):
            context_parts.append("\n\n=== SALES DATA (Sample) ===")
            sales_data = self._retrieve_sales_data({"limit": 5})
            context_parts.append(sales_data)
        
        if any(word in query_lower for word in ["customer", "client", "buyer", "order"]):
            context_parts.append("\n\n=== CUSTOMER DATA (Sample) ===")
            customer_data = self._retrieve_customer_data({"limit": 5})
            context_parts.append(customer_data)
        
        if any(word in query_lower for word in ["product", "item", "category"]):
            context_parts.append("\n\n=== PRODUCT DATA (Sample) ===")
            product_data = self._retrieve_product_data({"limit": 5})
            context_parts.append(product_data)
        
        return "\n".join(context_parts)
    
    def query(self, question: str) -> str:
        """
        Query the RAG system with a natural language question
        
        Args:
            question: Natural language question about retail analytics
            
        Returns:
            AI-generated response based on retrieved data
        """
        print(f"\n📊 Processing query: {question}")
        
        # Retrieve relevant context
        print("🔍 Retrieving context from gold tables...")
        context = self._create_retrieval_context(question)
        
        # Create prompt for Gemini
        system_prompt = """You are an expert retail analytics assistant. You have access to a retail and e-commerce analytics platform with gold-layer tables containing:
- Fact tables: Sales transactions, Returns
- Dimension tables: Customers, Products, Stores, Employees, Dates, Discounts

Your role is to:
1. Analyze the provided data and context
2. Answer questions about sales, customers, products, and store performance
3. Provide actionable insights and recommendations
4. Be specific with numbers and data points
5. Explain trends and patterns

Always cite specific data when available and be clear about any assumptions you make."""
        
        user_prompt = f"""Based on the following data from our retail analytics platform, please answer this question:

QUESTION: {question}

AVAILABLE DATA AND CONTEXT:
{context}

Please provide a comprehensive answer that:
1. Directly addresses the question
2. Uses specific numbers from the data when available
3. Provides business insights or recommendations
4. Is clear and actionable"""
        
        print("🤖 Generating response from Gemini...")
        
        try:
            # Call Gemini API
            response = self.model.generate_content(
                [system_prompt, user_prompt],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    max_output_tokens=2048
                )
            )
            
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def query_with_sql(self, question: str, sql_query: str) -> str:
        """
        Query with a specific SQL query to retrieve data
        
        Args:
            question: Natural language question
            sql_query: SQL query to execute against gold tables
            
        Returns:
            AI-generated response based on SQL results
        """
        print(f"\n📊 Processing query with SQL: {question}")
        
        # Execute SQL query
        print(f"🔍 Executing SQL query...")
        try:
            result_df = self.spark.sql(sql_query)
            sql_result = result_df.toPandas().to_json(orient="records")
        except Exception as e:
            return f"Error executing SQL query: {str(e)}"
        
        # Create prompt for Gemini
        system_prompt = """You are an expert retail analytics assistant with access to detailed sales, customer, and product data."""
        
        user_prompt = f"""Based on the following query results, please answer this question:

QUESTION: {question}

SQL QUERY EXECUTED:
{sql_query}

RESULTS:
{sql_result}

Please provide a comprehensive analysis with specific numbers and actionable insights."""
        
        print("🤖 Generating response from Gemini...")
        
        try:
            response = self.model.generate_content(
                [system_prompt, user_prompt],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    max_output_tokens=2048
                )
            )
            
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def multi_turn_conversation(self) -> None:
        """
        Interactive multi-turn conversation mode
        """
        print("\n" + "="*60)
        print("🎯 Retail Analytics RAG - Interactive Mode")
        print("="*60)
        print("Ask questions about your retail data. Type 'exit' to quit.\n")
        
        conversation_history = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\n👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Add to conversation history
                conversation_history.append({"role": "user", "content": user_input})
                
                # Get response
                response = self.query(user_input)
                conversation_history.append({"role": "assistant", "content": response})
                
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}\n")
