import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator

spark_conn = os.environ.get("spark_conn", "spark_conn")
spark_master = "spark://spark:7077"  
postgres_driver_jar = "/usr/local/spark/assets/jars/postgresql-42.2.6.jar"

with open("/usr/local/spark/assets/script/sql/ddl.sql", "r") as file:
    ddl_sql = file.read()

categoria_file = "/usr/local/spark/assets/data/CATEGORIA.csv"
cidade_file = "/usr/local/spark/assets/data/CIDADE.csv"
estado_file = "/usr/local/spark/assets/data/ESTADO.csv"
imovel_file = "/usr/local/spark/assets/data/IMOVEL.csv"
locacao_file = "/usr/local/spark/assets/data/LOCACAO.csv"
localizacao_file = "/usr/local/spark/assets/data/LOCALIZACAO.csv"
pessoas_file = "/usr/local/spark/assets/data/PESSOAS.csv"
postgres_db = "jdbc:postgresql://postgres:5432/airflow"
postgres_user = "airflow"
postgres_pwd = "airflow"

now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id="spark-postgres",
    description="This DAG is a sample of integration between Spark and DB. It reads CSV files, load them into a Postgres DB and then read them from the same Postgres DB.",
    default_args=default_args,
    schedule_interval=timedelta(1)
)

start = DummyOperator(task_id="start", dag=dag)

spark_job_load_postgres = SparkSubmitOperator(
    task_id="spark_job_load_postgres",
    application="/usr/local/spark/applications/load_postgres.py",
    name="load-postgres",
    conn_id=spark_conn,
    verbose=True,
    conf={
        "spark.master": spark_master,
        "spark.driver.extraClassPath": postgres_driver_jar,
        "spark.executor.extraClassPath": postgres_driver_jar
    },
    application_args=[categoria_file, cidade_file, estado_file, imovel_file,
                      locacao_file, localizacao_file, pessoas_file,
                      postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    dag=dag)

create_tables = PostgresOperator(
    task_id="create_tables",
    postgres_conn_id="postgres_conn", 
    sql=ddl_sql,  
    dag=dag)

end = DummyOperator(task_id="end", dag=dag)

start >> create_tables >> spark_job_load_postgres >> end
