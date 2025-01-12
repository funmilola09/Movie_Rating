from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2

# Define PostgreSQL connection
POSTGRES_CONN = {
    "host": "postgres",
    "database": "movie_ratings",
    "user": "airflow",
    "password": "airflow"
}

def extract_data(**kwargs):
    """Extract data from the CSV file."""
    df = pd.read_csv('/usr/local/airflow/data/movies.csv')
    kwargs['ti'].xcom_push(key='extracted_data', value=df.to_dict())

def transform_data(**kwargs):
    """Transform data to calculate average ratings."""
    data = kwargs['ti'].xcom_pull(key='extracted_data', task_ids='extract_data')
    df = pd.DataFrame(data)
    df['rating'] = pd.to_numeric(df['rating'])
    result = df.groupby(['movie_id', 'title']).rating.mean().reset_index()
    kwargs['ti'].xcom_push(key='transformed_data', value=result.to_dict())

def load_data(**kwargs):
    """Load transformed data into PostgreSQL."""
    data = kwargs['ti'].xcom_pull(key='transformed_data', task_ids='transform_data')
    df = pd.DataFrame(data)
    conn = psycopg2.connect(**POSTGRES_CONN)
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO movie_ratings (movie_id, title, average_rating) VALUES (%s, %s, %s)",
            (row['movie_id'], row['title'], row['rating']),
        )
    conn.commit()
    cursor.close()
    conn.close()

default_args = {"start_date": datetime(2023, 1, 1)}
dag = DAG("movie_ratings_pipeline", default_args=default_args, schedule_interval="@daily")

with dag:
    extract_task = PythonOperator(task_id="extract_data", python_callable=extract_data)
    transform_task = PythonOperator(task_id="transform_data", python_callable=transform_data)
    load_task = PythonOperator(task_id="load_data", python_callable=load_data)

    extract_task >> transform_task >> load_task
