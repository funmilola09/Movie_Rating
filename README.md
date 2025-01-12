**Movie Ratings ETL Pipeline**
This repository contains an Apache Airflow ETL pipeline for processing movie rating data. 
The pipeline reads raw data from a CSV file, transforms it to calculate average ratings for each movie, and loads the results into a PostgreSQL database.

**Features**
Data Extraction: Reads raw movie rating data from a CSV file.
Data Transformation: Calculates the average rating for each movie.
Data Loading: Inserts the transformed data into a PostgreSQL database.


**Technologies Used**
Python: Core language for the ETL logic.
Apache Airflow: Workflow orchestration and scheduling.
Pandas: Data processing and transformation.
PostgreSQL: Database for storing transformed data.
psycopg2: Python library for PostgreSQL database connection.
