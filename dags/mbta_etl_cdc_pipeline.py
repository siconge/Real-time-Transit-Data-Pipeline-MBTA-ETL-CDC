import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.time_delta import TimeDeltaSensor

# Set the path to include the parent directory for module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etls.mbta_etl import call_mbta_api, mbta_api_timeloop
from cdc.mysql_binlog import capture_mysql_binlog
from cdc.mysql_mongo_scheduler import initial_timestamp, cdc_timeloop

default_args = {
    'owner': 'Sicong E',
    'start_date': datetime(2024, 1, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'execution_timeout': timedelta(hours=24)
}

dag = DAG(
    dag_id='etl_cdc_mbta_pipeline',
    default_args=default_args,
    description='ETL from MBTA API to MySQL; CDC from MySQL to MongoDB and binlog',
    schedule_interval='@weekly',
    catchup=0,
    tags=['mbta', 'etl', 'cdc', 'pipeline']
)

# Task to remove existing Docker containers for MySQL and MongoDB to ensure a clean state
remove_containers = BashOperator(
    task_id='remove_containers',
    bash_command='python3 containers.py -remove',
    dag=dag
)

# Task to create Docker containers for MySQL and MongoDB
create_containers = BashOperator(
    task_id='create_containers',
    bash_command='python3 containers.py -create',
    dag=dag
)

# Task to initialize the record list by making the first API call to MBTA
initialize_records = PythonOperator(
    task_id='initialize_records',
    python_callable=call_mbta_api,
    dag=dag
)

# Task to start CDC timeloop for data sync between MySQL and MongoDB
cdc_mysql_mongo = PythonOperator(
    task_id='start_cdc_mysql_mongo',
    python_callable=cdc_timeloop,
    op_kwargs={'last_check_stamp':initial_timestamp()},
    dag=dag
)

# Task to make API calls to MBTA every 10 seconds and conduct data ETLs
api_timeloop = PythonOperator(
    task_id='start_api_timeloop',
    python_callable=mbta_api_timeloop,
    dag=dag
)

# Task to start CDC timeloop for capturing MySQL binlog
cdc_mysql_binlog = PythonOperator(
    task_id='start_cdc_mysql_binlog',
    python_callable=capture_mysql_binlog,
    dag=dag
)

# Task to handle time delays and maintain clear separation of tasks
delay_next_task = TimeDeltaSensor(
    task_id='delay_next_task',
    delta=timedelta(seconds=30),
    dag=dag
)

# Define the task dependencies
remove_containers >> delay_next_task >> create_containers >> delay_next_task >> initialize_records >> [api_timeloop, cdc_mysql_mongo, cdc_mysql_binlog]