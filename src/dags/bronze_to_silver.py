import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

spark_conn = os.environ.get("spark_conn", "spark_conn")
spark_master = "spark://spark:7077"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'bronze_to_silver',
    default_args=default_args,
    description='Process data from bronze to silver layer',
    schedule_interval='@daily',
    catchup=False
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

bronze_to_silver = SparkSubmitOperator(
    task_id='bronze_to_silver',
    application='/usr/local/spark/applications/bronze_to_silver.py',
    name='bronze_to_silver',
    conn_id=spark_conn,
    verbose=True,
    conf={
        "spark.master": spark_master,
        "spark.jars.packages": "io.delta:delta-core_2.12:1.0.0,org.apache.hadoop:hadoop-aws:3.2.0",
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark.hadoop.fs.s3a.endpoint": "http://bucket:9000",
        "spark.hadoop.fs.s3a.access.key": "airflow",
        "spark.hadoop.fs.s3a.secret.key": "airflow",
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem"
    },
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

start >> bronze_to_silver >> end
