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