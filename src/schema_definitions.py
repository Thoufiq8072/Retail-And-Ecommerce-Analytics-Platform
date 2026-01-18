SILVER_CUSTOMERS_SCHEMA = {
    "customer_id":"integer",
    "name":"string",
    "email":"string",
    "telephone":"string",
    "city":"string",
    "country":"string",
    "gender":"string",
    "date_of_birth":"date",
    "job_title":"string"
}

SILVER_DISCOUNTS_SCHEMA = {
    "discount_start_date":"date",
    "discount_end_date":"date",
    "discount":"double",
    "description":"string",
    "category":"string",
    "sub_category":"string"
}

SILVER_EMPLOYEES_SCHEMA = {
    "employee_id":"integer",
    "store_id":"integer",
    "name":"string",
    "position":"string"
}

SILVER_PRODUCTS_SCHEMA = {
    "product_id":"integer",
    "category":"string",
    "sub_category":"string",
    "description_PT":"string",
    "description_DE":"string",
    "description_FR":"string",
    "description_ES":"string",
    "description_EN":"string",
    "description_ZH":"string",
    "color":"string",
    "sizes":"string",
    "production_cost":"double"
}

SILVER_STORES_SCHEMA = {
    "store_id":"integer",
    "country":"string",
    "city":"string",
    "store_name":"string",
    "number_of_employees":"integer",
    "zip_code":"string",
    "latitude":"double",
    "longitude":"double"
}

SILVER_TRANSACTIONS_SCHEMA = {
    "invoice_id":"string",
    "line":"integer",
    "customer_id":"integer",
    "product_id":"integer",
    "size":"string",
    "color":"string",
    "unit_price":"double",
    "quantity":"integer",
    "date":"timestamp",
    "discount":"double",
    "line_total":"double",
    "store_id":"integer",
    "employee_id":"integer",
    "currency":"string",
    "currency_symbol":"string",
    "sku":"string",
    "transaction_type":"string",
    "payment_method":"string",
    "invoice_total":"double"
}


DIM_DATES_SCHEMA = {
    "date_sk":"integer",
    "date":"date",
    "day":"integer",
    "month":"integer",
    "month_name":"string",
    "quarter":"integer",
    "year":"integer",
    "day_of_week":"integer",
    "day_name":"string",
    "is_weekend":"boolean"
}


DIM_CUSTOMERS_SCHEMA = {
    "customer_sk":"long",
    "customer_id":"integer",
    "name":"string",
    "email":"string",
    "telephone":"string",
    "city":"string",
    "country":"string",
    "gender":"string",
    "date_of_birth":"date",
    "job_title":"string",
    "_created_at":"timestamp",
    "_updated_at":"timestamp"
}


DIM_PRODUCTS_SCHEMA = {
    "product_sk":"long",
    "product_id":"integer",
    "category":"string",
    "sub_category":"string",
    "color":"string",
    "sizes":"string",
    "production_cost":"double",
    "description_PT":"string",
    "description_DE":"string",
    "description_FR":"string",
    "description_ES":"string",
    "description_EN":"string",
    "description_ZH":"string",
    "_created_at":"timestamp",
    "_updated_at":"timestamp"
}


DIM_STORES_SCHEMA = {
    "store_sk":"long",
    "store_id":"integer",
    "store_name":"string",
    "city":"string",
    "country":"string",
    "zip_code":"string",
    "latitude":"double",
    "longitude":"double",
    "number_of_employees":"integer",
    "_created_at":"timestamp",
    "_updated_at":"timestamp"
}


DIM_EMPLOYEES_SCHEMA = {
    "employee_sk":"long",
    "employee_id":"integer",
    "store_id":"integer",
    "name":"string",
    "position":"string",
    "_created_at":"timestamp",
    "_updated_at":"timestamp"
}


DIM_DISCOUNTS_SCHEMA = {
    "discount_sk":"long",
    "discount_start_date":"date",
    "discount_end_date":"date",
    "discount":"double",
    "description":"string",
    "category":"string",
    "sub_category":"string",
    "_created_at":"timestamp",
    "_updated_at":"timestamp"
}


FACT_SALES_SCHEMA = {
    "sales_sk":"long",
    "date_sk":"integer",
    "customer_sk":"long",
    "product_sk":"long",
    "store_sk":"long",
    "employee_sk":"long",
    "discount_sk":"long",
    "invoice_id":"string",
    "line":"integer",
    "size":"string",
    "unit_price":"double",
    "quantity":"integer",
    "line_total":"double",
    "invoice_total":"double",
    "currency":"string",
    "payment_method":"string",
    "sale_date":"timestamp",
    "_created_at": "timestamp"
}


FACT_RETURNS_SCHEMA = {
    "return_sk":"long",
    "date_sk":"integer",
    "customer_sk":"long",
    "product_sk":"long",
    "store_sk":"long",
    "employee_sk":"long",
    "invoice_id":"string",
    "line":"integer",
    "size":"string",
    "quantity_returned":"integer",
    "refund_amount":"double",
    "currency":"string",
    "sale_date":"timestamp",
    "_created_at": "timestamp"
}
