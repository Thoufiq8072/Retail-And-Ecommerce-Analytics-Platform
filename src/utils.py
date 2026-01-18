from pyspark.sql.functions import *
from pyspark.sql.types import *

def add_ingestion_timestamp(df):
    """ It will create ingestion_ts and _source_file columns for bronze table metadata"""
    df = df.withColumn("ingestion_ts", current_timestamp()).withColumn("_source_file", col("_metadata.file_path"))
    return df


def add_gold_metadata(df):
    """ It will create _created_at and _updated_at columns for gold table metadata"""
    df = df.withColumn("_created_at", current_timestamp()).withColumn("_updated_at", current_timestamp())
    return df
