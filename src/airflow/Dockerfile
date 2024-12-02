# Base Image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Airflow requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies for Airflow
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy DAG files to the Airflow DAGs directory
COPY dags /usr/local/airflow/dags

# Set the default command to run the Airflow webserver
CMD ["airflow", "webserver"]
