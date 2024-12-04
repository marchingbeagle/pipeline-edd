from pyspark.sql import SparkSession
from pyspark.sql.functions import (current_timestamp, lit, regexp_replace, 
                                 when, col, trim, to_timestamp, date_format)
from pyspark.sql.types import *
from datetime import datetime
import unicodedata

def create_spark_session():
    return SparkSession.builder \
        .appName("LandingToBronze") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

def get_schema(table_name):
    schemas = {
        "pessoas": StructType([
            StructField("idpessoas", IntegerType(), True),
            StructField("nome", StringType(), False),
            StructField("cpf", StringType(), False),
            StructField("data_nascimento", TimestampType(), False),
            StructField("endereco", StringType(), False),
            StructField("telefone", StringType(), False),
            StructField("sexo", StringType(), False)
        ]),
        "log": StructType([
            StructField("idlog", IntegerType(), True),
            StructField("titulo", StringType(), False),
            StructField("descricao", StringType(), False),
            StructField("data", TimestampType(), False)
        ]),
        "estado": StructType([
            StructField("idestado", IntegerType(), True),
            StructField("nome_estado", StringType(), False),
            StructField("sigla_estado", StringType(), False)
        ]),
        "cidade": StructType([
            StructField("idcidade", IntegerType(), True),
            StructField("nome", StringType(), False),
            StructField("estado", IntegerType(), False)
        ]),
        "categoria": StructType([
            StructField("idcategoria", IntegerType(), True),
            StructField("nome", StringType(), True),
            StructField("descricao", StringType(), True),
            StructField("data_criacao", TimestampType(), True),
            StructField("data_atualizacao", TimestampType(), True)
        ]),
        "localizacao": StructType([
            StructField("idlocalizacao", IntegerType(), True),
            StructField("cep", StringType(), False),
            StructField("numero_imovel", StringType(), False),
            StructField("complemento", StringType(), True),
            StructField("referencia", StringType(), True),
            StructField("cidade", IntegerType(), True),
            StructField("categoria", IntegerType(), True)
        ]),
        "imovel": StructType([
            StructField("idimovel", IntegerType(), True),
            StructField("localizacao", IntegerType(), True),
            StructField("proprietario", IntegerType(), True),
            StructField("preco_compra", IntegerType(), True),
            StructField("preco_aluguel", IntegerType(), True)
        ]),
        "locacao": StructType([
            StructField("idlocacao", IntegerType(), True),
            StructField("inquilino", IntegerType(), False),
            StructField("valor_contrato", IntegerType(), False),
            StructField("vigencia", TimestampType(), False),
            StructField("localizacao", IntegerType(), False),
            StructField("corretor", IntegerType(), False),
            StructField("imovel", IntegerType(), False)
        ])
    }
    return schemas.get(table_name)

def clean_text_columns(df):
    """Remove special characters and standardize text"""
    string_columns = [f.name for f in df.schema.fields if isinstance(f.dataType, StringType)]
    
    for col_name in string_columns:
        df = df.withColumn(col_name, 
            regexp_replace(trim(col(col_name)), r'[^\w\s-]', ''))
    return df

def validate_required_fields(df, table_name):
    """Check for required fields based on schema"""
    schema = get_schema(table_name)
    if schema:
        for field in schema.fields:
            if not field.nullable:
                df = df.filter(col(field.name).isNotNull())
    return df

def add_metadata(df, table_name):
    """Add tracking metadata"""
    return df \
        .withColumn("processing_date", current_timestamp()) \
        .withColumn("source_layer", lit("landing")) \
        .withColumn("source_file", lit(f"{table_name}")) \
        .withColumn("batch_id", date_format(current_timestamp(), "yyyyMMdd_HHmmss"))

def process_table(spark, table_name):
    df = spark.read.format("delta").load(f"s3a://landing/{table_name}")
    
    df_cleaned = df \
        .dropDuplicates() \
        .na.drop(subset=[col for col, dtype in df.dtypes if dtype != 'string']) 
    
    df_cleaned = clean_text_columns(df_cleaned)
    
    df_validated = validate_required_fields(df_cleaned, table_name)
    
    df_processed = add_metadata(df_validated, table_name)
    
    success_count = df_processed.count()
    total_count = df.count()
    
    df_processed.write \
        .format("delta") \
        .mode("overwrite") \
        .option("userMetadata", f"Records processed: {success_count}/{total_count}") \
        .save(f"s3a://bronze/{table_name}")
    
    return success_count, total_count

def main():
    spark = create_spark_session()
    
    tables = ["categoria", "cidade", "estado", "imovel", 
              "locacao", "localizacao", "pessoas"]
    
    for table in tables:
        try:
            success_count, total_count = process_table(spark, table)
            print(f"Table: {table}")
            print(f"Successfully processed: {success_count}/{total_count} records")
            print(f"Quality ratio: {(success_count/total_count)*100:.2f}%")
        except Exception as e:
            print(f"Error processing table {table}: {str(e)}")
    
    spark.stop()

if __name__ == "__main__":
    main()
