import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_unixtime, col, to_timestamp
from pyspark.sql.types import DoubleType

# Create spark session
spark = (SparkSession
         .builder
         .master("spark://spark:7077")  # Add explicit master URL
         .appName("load-postgres")      # Add application name
         .config("spark.jars", "/usr/local/spark/assets/jars/postgresql-42.2.6.jar")
         .getOrCreate()
         )

categoria_file = sys.argv[1]
cidade_file = sys.argv[2]
estado_file = sys.argv[3]
imovel_file = sys.argv[4]
locacao_file = sys.argv[5]
localizacao_file = sys.argv[6]
pessoas_file = sys.argv[7]
postgres_db = sys.argv[8]
postgres_user = sys.argv[9]
postgres_pwd = sys.argv[10]

print("######################################")
print("READING CSV FILES")
print("######################################")

df_categoria_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(categoria_file)
)

df_cidade_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(cidade_file)
)

df_estado_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(estado_file)
)

df_imovel_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(imovel_file)
)

df_locacao_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(locacao_file)
)

df_localizacao_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(localizacao_file)
)

df_pessoas_csv = (
    spark.read
    .format("csv")
    .option("header", True)
    .load(pessoas_file)
)

print("######################################")
print("LOADING POSTGRES TABLES")
print("######################################")

(
    df_categoria_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.categoria")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)

(
    df_cidade_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.cidade")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)

(
    df_estado_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.estado")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)

(
    df_imovel_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.imovel")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)

(
    df_locacao_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.locacao")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)

(
    df_localizacao_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.localizacao")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)

(
    df_pessoas_csv.write
    .format("jdbc")
    .option("url", postgres_db)
    .option("dbtable", "public.pessoas")
    .option("user", postgres_user)
    .option("password", postgres_pwd)
    .mode("overwrite")
    .save()
)
