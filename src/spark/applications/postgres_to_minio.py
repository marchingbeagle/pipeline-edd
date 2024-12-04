import sys
from pyspark.sql import SparkSession
import time

def create_spark_session():
    return (SparkSession
            .builder
            .appName("postgres-to-minio")
            .config("spark.master", "spark://spark:7077")
            .config("spark.hadoop.fs.s3a.endpoint", "http://bucket:9000")
            .config("spark.hadoop.fs.s3a.access.key", "airflow")
            .config("spark.hadoop.fs.s3a.secret.key", "airflow")
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .config("spark.jars.packages", 
                   "io.delta:delta-core_2.12:1.0.0,"  
                   "org.postgresql:postgresql:42.2.6,"  
                   "org.apache.hadoop:hadoop-aws:3.2.0,"  
                   "com.amazonaws:aws-java-sdk-bundle:1.11.563")  
            .getOrCreate())

def read_postgres_table(spark, table, postgres_url, properties):
    try:
        return spark.read.format("jdbc") \
            .option("url", postgres_url) \
            .option("dbtable", table) \
            .option("user", properties["user"]) \
            .option("password", properties["password"]) \
            .option("driver", properties["driver"]) \
            .load()
    except Exception as e:
        print(f"Error reading table {table}: {str(e)}")
        return None

def write_table(df, table_name):
    if df is None:
        return False
    
    try:
        (df.write
         .format("delta")
         .mode("overwrite")
         .option("overwriteSchema", "true")
         .option("mergeSchema", "true")
         .option("delta.autoOptimize.optimizeWrite", "true")
         .option("delta.autoOptimize.autoCompact", "true")
         .save(f"s3a://landing/{table_name}"))
        return True
    except Exception as e:
        print(f"Error writing table {table_name}: {str(e)}")
        return False

def main():
    if len(sys.argv) != 4:
        print("Usage: <postgres_url> <postgres_user> <postgres_pwd>")
        sys.exit(1)
        
    postgres_url = sys.argv[1]
    postgres_user = sys.argv[2]
    postgres_pwd = sys.argv[3]

    tables = ["categoria", "cidade", "estado", "imovel", 
              "locacao", "localizacao", "pessoas"]

    spark = create_spark_session()
    
    properties = {
        "user": postgres_user,
        "password": postgres_pwd,
        "driver": "org.postgresql.Driver"
    }

    success_count = 0
    failure_count = 0

    for table in tables:
        print(f"Processing table: {table}")
        try:
            df = read_postgres_table(spark, table, postgres_url, properties)
            if write_table(df, table):
                success_count += 1
                print(f"Successfully processed table: {table}")
            else:
                failure_count += 1
                print(f"Failed to process table: {table}")
        except Exception as e:
            failure_count += 1
            print(f"Error processing table {table}: {str(e)}")
            continue

    print(f"\nProcessing complete. Successful: {success_count}, Failed: {failure_count}")
    
    if failure_count > 0:
        sys.exit(1)
        
    spark.stop()

if __name__ == "__main__":
    main()
