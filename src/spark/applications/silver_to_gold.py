from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, sum, count, avg, month, year, 
                                 datediff, months_between, current_date,
                                 desc, dense_rank, window, current_timestamp, lag)
from pyspark.sql.window import Window
from datetime import datetime

def create_spark_session():
    return SparkSession.builder \
        .appName("SilverToGold") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

def create_dim_localizacao(spark):
    return spark.read.format("delta").load("s3a://silver/localizacao") \
        .join(spark.read.format("delta").load("s3a://silver/cidade"), "cidade") \
        .join(spark.read.format("delta").load("s3a://silver/estado"), "estado") \
        .selectExpr(
            "idlocalizacao",
            "cep",
            "cidade.nome as cidade_nome",
            "estado.nome_estado",
            "estado.sigla_estado"
        )

def create_dim_pessoas(spark):
    return spark.read.format("delta").load("s3a://silver/pessoas") \
        .selectExpr(
            "idpessoas",
            "nome",
            "cpf",
            "data_nascimento"
        )

def create_fact_locacao(spark):
    locacao = spark.read.format("delta").load("s3a://silver/locacao")
    imovel = spark.read.format("delta").load("s3a://silver/imovel")
    
    return locacao.join(imovel, "imovel") \
        .selectExpr(
            "idlocacao",
            "imovel",
            "inquilino",
            "valor_contrato",
            "vigencia",
            "corretor",
            "localizacao",
            "preco_aluguel"
        )

def create_analytical_views(spark):
    avg_rent = spark.read.format("delta").load("s3a://gold/fact_locacao") \
        .join(spark.read.format("delta").load("s3a://gold/dim_localizacao"), "localizacao") \
        .groupBy("cidade_nome", "nome_estado") \
        .agg(
            avg("valor_contrato").alias("aluguel_medio"),
            count("*").alias("total_locacoes")
        )
    
    w_spec = Window.orderBy(desc("total_contratos"))
    top_corretores = spark.read.format("delta").load("s3a://gold/fact_locacao") \
        .join(spark.read.format("delta").load("s3a://gold/dim_pessoas"), col("corretor") == col("idpessoas")) \
        .groupBy("corretor", "nome") \
        .agg(
            count("*").alias("total_contratos"),
            sum("valor_contrato").alias("valor_total")
        ) \
        .withColumn("ranking", dense_rank().over(w_spec))
    
    avg_rent.write.format("delta").mode("overwrite").save("s3a://gold/view_aluguel_medio_regiao")
    top_corretores.write.format("delta").mode("overwrite").save("s3a://gold/view_top_corretores")

def create_kpi_views(spark):
    fact_locacao = spark.read.format("delta").load("s3a://gold/fact_locacao")
    dim_localizacao = spark.read.format("delta").load("s3a://gold/dim_localizacao")
    dim_imovel = spark.read.format("delta").load("s3a://silver/imovel")
    
    # 1. Receita Total de Locações
    receita_total = fact_locacao \
        .groupBy(year("vigencia").alias("ano"), month("vigencia").alias("mes")) \
        .agg(
            sum("valor_contrato").alias("receita_total"),
            count("*").alias("numero_contratos")
        )
    
    # 2. Imóveis Alugados por Cidade
    imoveis_cidade = fact_locacao \
        .join(dim_localizacao, "localizacao") \
        .groupBy("cidade_nome", "nome_estado") \
        .agg(
            count("*").alias("total_imoveis_alugados"),
            sum("valor_contrato").alias("receita_total_cidade")
        )
    
    # 3. Taxa de Ocupação
    total_imoveis = dim_imovel.count()
    taxa_ocupacao = fact_locacao \
        .join(dim_localizacao, "localizacao") \
        .groupBy("cidade_nome") \
        .agg(
            (count("*") / total_imoveis * 100).alias("taxa_ocupacao"),
            count("*").alias("imoveis_ocupados")
        )
    
    # 4. Duração Média dos Contratos
    duracao_contratos = fact_locacao \
        .withColumn("duracao_meses", months_between(col("vigencia"), current_date())) \
        .groupBy(year("vigencia"), month("vigencia")) \
        .agg(
            avg("duracao_meses").alias("duracao_media_meses")
        )
    
    # Métricas detalhadas
    # 1. Valor Médio por Metro Quadrado
    valor_metro = fact_locacao \
        .join(dim_imovel, "imovel") \
        .join(dim_localizacao, "localizacao") \
        .groupBy("cidade_nome", "nome_estado") \
        .agg(
            (avg("valor_contrato") / avg("area")).alias("valor_medio_metro"),
            avg("valor_contrato").alias("valor_medio_total")
        )
    
    # 2. Variação Mensal
    window_spec = Window.partitionBy("cidade_nome").orderBy("ano", "mes")
    variacao_mensal = fact_locacao \
        .join(dim_localizacao, "localizacao") \
        .groupBy("cidade_nome", year("vigencia").alias("ano"), month("vigencia").alias("mes")) \
        .agg(avg("valor_contrato").alias("valor_medio")) \
        .withColumn("variacao_anterior", 
            (col("valor_medio") - lag("valor_medio", 1).over(window_spec)) / lag("valor_medio", 1).over(window_spec) * 100)
    
    # Salvar views para o dashboard
    receita_total.write.format("delta").mode("overwrite").save("s3a://gold/kpi_receita_total")
    imoveis_cidade.write.format("delta").mode("overwrite").save("s3a://gold/kpi_imoveis_cidade")
    taxa_ocupacao.write.format("delta").mode("overwrite").save("s3a://gold/kpi_taxa_ocupacao")
    duracao_contratos.write.format("delta").mode("overwrite").save("s3a://gold/kpi_duracao_contratos")
    valor_metro.write.format("delta").mode("overwrite").save("s3a://gold/metric_valor_metro")
    variacao_mensal.write.format("delta").mode("overwrite").save("s3a://gold/metric_variacao_mensal")

def main():
    spark = create_spark_session()
    
    try:
        dim_localizacao = create_dim_localizacao(spark)
        dim_pessoas = create_dim_pessoas(spark)
        fact_locacao = create_fact_locacao(spark)
        
        dim_localizacao.write.format("delta").mode("overwrite").save("s3a://gold/dim_localizacao")
        dim_pessoas.write.format("delta").mode("overwrite").save("s3a://gold/dim_pessoas")
        fact_locacao.write.format("delta").mode("overwrite").save("s3a://gold/fact_locacao")
        
        create_analytical_views(spark)
        create_kpi_views(spark)
        
        print("Gold layer processing completed successfully")
        
    except Exception as e:
        print(f"Error processing gold layer: {str(e)}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
