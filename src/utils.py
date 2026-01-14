from pyspark.sql.functions import *
from pyspark.sql.types import *

def add_ingestion_timestamp(df):
    df = df.withColumn("ingestion_ts", current_timestamp()).withColumn("_source_file", col("_metadata.file_path"))
    return df
