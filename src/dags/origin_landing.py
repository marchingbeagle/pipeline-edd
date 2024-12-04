import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

spark_conn = os.environ.get("spark_conn", "spark_conn")
spark_master = "spark://spark:7077"

postgres_db = "jdbc:postgresql://postgres:5432/airflow"
postgres_user = "airflow"
postgres_pwd = "airflow"

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
    'postgres_to_minio_delta',
    default_args=default_args,
    description='Copy data from Postgres to MinIO in Delta format',
    schedule_interval='@daily',
    catchup=False
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

postgres_to_minio = SparkSubmitOperator(
    task_id='postgres_to_minio',
    application='/usr/local/spark/applications/postgres_to_minio.py',
    name='postgres_to_minio',
    conn_id=spark_conn,
    verbose=True,
    conf={
        "spark.master": spark_master,
        "spark.jars.packages": "io.delta:delta-core_2.12:1.0.0,org.apache.hadoop:hadoop-aws:3.2.0,com.amazonaws:aws-java-sdk-bundle:1.11.563,org.postgresql:postgresql:42.2.6",
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark.hadoop.fs.s3a.endpoint": "http://bucket:9000",
        "spark.hadoop.fs.s3a.access.key": "airflow",
        "spark.hadoop.fs.s3a.secret.key": "airflow",
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem"
    },
    application_args=[postgres_db, postgres_user, postgres_pwd],
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

start >> postgres_to_minio >> end