import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count, lit
import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# Setup Spark Session
def create_spark_session():
    return SparkSession.builder \
        .appName("SoccerBatchProcessing") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.2.14") \
        .getOrCreate()

def load_data_from_postgres(spark, jdbc_url, db_table, properties):
    """Loads data from PostgreSQL using JDBC."""
    try:
        df = spark.read.jdbc(url=jdbc_url, table=db_table, properties=properties)
        logging.info(f"Successfully loaded data from PostgreSQL table: {db_table}")
        return df
    except Exception as e:
        logging.error(f"Error loading data from PostgreSQL: {e}")
        raise

def transform_data(df):
    """Transform the raw soccer match data."""
    try:
        # Example transformation: Adding a new column 'match_status' based on state_id
        df = df.withColumn("match_status", when(col("state_id") == 1, "Scheduled")
                           .when(col("state_id") == 2, "Ongoing")
                           .when(col("state_id") == 3, "Completed")
                           .otherwise("Unknown"))

        # Example aggregation: Average length of matches per league
        avg_match_length_df = df.groupBy("league_id").agg(avg("length").alias("avg_match_length"))
        
        # Example feature engineering: Total number of matches per venue
        matches_per_venue_df = df.groupBy("venue_id").agg(count("*").alias("total_matches"))
        
        # Join the transformed data back to create a comprehensive dataframe
        transformed_df = df.join(avg_match_length_df, "league_id", "left") \
                           .join(matches_per_venue_df, "venue_id", "left")

        return transformed_df
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        raise

def write_data_to_gcs(df, output_path):
    """Writes the transformed data back to GCS in Parquet format."""
    try:
        df.write.mode("overwrite").parquet(output_path)
        logging.info(f"Successfully wrote transformed data to GCS at: {output_path}")
    except Exception as e:
        logging.error(f"Error writing data to GCS: {e}")
        raise

if __name__ == "__main__":
    # Initialize Spark session
    spark = create_spark_session()

    # PostgreSQL connection properties
    jdbc_url = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    db_table = "soccer_matches"
    properties = {
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
        "driver": "org.postgresql.Driver"
    }
    
    try:
        # Step 1: Load data from PostgreSQL
        soccer_df = load_data_from_postgres(spark, jdbc_url, db_table, properties)

        # Step 2: Transform the data
        transformed_df = transform_data(soccer_df)

        # Step 3: Write the transformed data back to GCS
        output_path = "gs://soccer_data_bucket/transformed_data/soccer_matches"
        write_data_to_gcs(transformed_df, output_path)

    except Exception as e:
        logging.error(f"ETL job failed: {e}")
    finally:
        spark.stop()
