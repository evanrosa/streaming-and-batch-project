# European Soccer Data Platform

#### This project is in progress.

This project is a data platform designed for analyzing European soccer data. It leverages a modern data stack including Apache Airflow, Apache Spark, Confluent Kafka, and Apache Flink, all orchestrated using Docker and GCP. The platform is built with Python and aims to provide a scalable and efficient solution for processing and analyzing soccer data.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The platform ingests live soccer data from external APIs, processes it using Kafka and Flink, and stores it in a database/warehosue. The data is then transformed and analyzed using Spark, with results visualized in Grafana dashboards.

## Architecture

The architecture consists of several key components:

- **Kafka**: Used for real-time data streaming and message brokering.
- **Flink**: Processes streaming data from Kafka.
- **Spark**: Performs batch processing and data transformation.
- **Airflow**: Orchestrates ETL workflows.
- **PostgreSQL**: Stores processed data.
- **Grafana**: Visualizes data through dashboards.

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose
- Python 3.10+
- Java 11 (for Flink)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/soccer-data-platform.git
   cd soccer-data-platform
   ```

2. **Environment Configuration**

   Set up your environment variables in a `.env` file. Refer to the `.env.example` for required variables.

3. **Build and Start Services**

   Use Docker Compose to build and start all services:

   ```bash
   docker-compose up --build
   ```

4. **Initialize Database**

   Ensure the PostgreSQL database is initialized with the necessary tables:

   ```sql:src/sql/init.sql
   startLine: 1
   endLine: 34
   ```

## Usage

### Running the Platform

- **Airflow**: Access the Airflow web UI at `http://localhost:<AIRFLOW_PORT>`.
- **Grafana**: Access Grafana dashboards at `http://localhost:<GRAFANA_PORT>`.

### Data Ingestion and Processing

- **Kafka Producer**: Produces live soccer data to Kafka topics.
- **Flink Job**: Processes data from Kafka and writes results back to Kafka.
- **Spark Job**: Transforms data and writes it to Google Cloud Storage.

### Example Commands

- Start Kafka Producer:

  ```bash
  docker-compose exec kafka-producer python producer.py
  ```

- Run Spark Job:

  ```bash
  docker-compose exec spark spark-submit src/spark/jobs/main_job.py
  ```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
