from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, when, to_timestamp, regexp_replace, 
                                 trim, upper, date_format, coalesce, lit, length, current_timestamp)
from pyspark.sql.types import *
from datetime import datetime

def create_spark_session():
    return SparkSession.builder \
        .appName("BronzeToSilver") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

def clean_cpf(df):
    return df.withColumn("cpf", 
        regexp_replace(col("cpf"), "[^0-9]", ""))

def clean_phone(df):
    return df.withColumn("telefone", 
        regexp_replace(col("telefone"), "[^0-9]", ""))

def validate_date(df, date_column):
    return df.withColumn(date_column,
        when(col(date_column).cast("timestamp").isNotNull(), 
             col(date_column)).otherwise(None))

def process_pessoas(spark):
    df = spark.read.format("delta").load("s3a://bronze/pessoas")
    
    return df \
        .dropDuplicates(["cpf"]) \
        .filter(col("cpf").isNotNull()) \
        .transform(clean_cpf) \
        .transform(clean_phone) \
        .transform(lambda df: validate_date(df, "data_nascimento")) \
        .withColumn("nome", trim(upper(col("nome"))))

def process_locacao(spark):
    df = spark.read.format("delta").load("s3a://bronze/locacao")
    
    # Join with imovel and pessoas for enrichment
    df_imovel = spark.read.format("delta").load("s3a://bronze/imovel")
    df_pessoas = spark.read.format("delta").load("s3a://bronze/pessoas")
    
    return df \
        .join(df_imovel, df.imovel == df_imovel.idimovel, "left") \
        .join(df_pessoas, df.inquilino == df_pessoas.idpessoas, "left") \
        .filter(col("valor_contrato") > 0) \
        .transform(lambda df: validate_date(df, "vigencia"))

def process_imovel(spark):
    df = spark.read.format("delta").load("s3a://bronze/imovel")
    df_loc = spark.read.format("delta").load("s3a://bronze/localizacao")
    
    return df \
        .join(df_loc, df.localizacao == df_loc.idlocalizacao, "left") \
        .filter(col("preco_aluguel") > 0) \
        .filter(col("preco_compra") > 0)

def process_localizacao(spark):
    df = spark.read.format("delta").load("s3a://bronze/localizacao")
    df_cidade = spark.read.format("delta").load("s3a://bronze/cidade")
    
    return df \
        .join(df_cidade, df.cidade == df_cidade.idcidade, "left") \
        .withColumn("cep", regexp_replace(col("cep"), "[^0-9]", "")) \
        .filter(length(col("cep")) == 8)

def process_table(spark, table_name):
    processors = {
        "pessoas": process_pessoas,
        "locacao": process_locacao,
        "imovel": process_imovel,
        "localizacao": process_localizacao
    }
    
    if table_name in processors:
        df_processed = processors[table_name](spark)
    else:
        # Default processing for other tables
        df_processed = spark.read.format("delta").load(f"s3a://bronze/{table_name}") \
            .dropDuplicates()
    
    # Add processing metadata
    df_final = df_processed \
        .withColumn("silver_processing_date", current_timestamp()) \
        .withColumn("silver_batch_id", date_format(current_timestamp(), "yyyyMMdd_HHmmss"))
    
    # Write to silver
    df_final.write \
        .format("delta") \
        .mode("overwrite") \
        .save(f"s3a://silver/{table_name}")

def main():
    spark = create_spark_session()
    
    tables = ["pessoas", "log", "estado", "cidade", 
              "categoria", "localizacao", "imovel", "locacao"]
    
    for table in tables:
        try:
            process_table(spark, table)
            print(f"Successfully processed {table} to silver layer")
        except Exception as e:
            print(f"Error processing {table}: {str(e)}")
    
    spark.stop()

if __name__ == "__main__":
    main()
