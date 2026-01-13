def add_ingestion_timestamp(df):
    df = df.withColumn("ingestion_ts", current_timestamp()).withColumn("_source_file", input_file_name())
    return df
