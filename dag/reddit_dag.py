import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

from Pipeline_function import reddit_pipeline
from Pipeline_function.aws_pipeline import upload_s3_pipeline

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

default_args = {
    'owner': 'Sushith Suthan',
    'start_date': datetime(2025, 6, 14)
}


file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id='etl_reddit_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['reddit', 'etl']
)

dag_start = DummyOperator(
    task_id='dag_start',
    dag=dag)


extract = PythonOperator(
    task_id='reddit_extraction',
    python_callable= reddit_pipeline,
    op_kwargs={
        'file_name': f'reddit_{file_postfix}',
        'subreddit': 'data_engineering',
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)


upload_s3 = PythonOperator(
    task_id='s3_upload',
    python_callable=upload_s3_pipeline,
    dag=dag
)
# Better use slack notifications

dag_end = DummyOperator(
    task_id='dag_end',
    dag=dag)

dag_start >> extract >> upload_s3 >> dag_end