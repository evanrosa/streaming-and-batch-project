# Base Image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy application files and Kafka consumer requirements
COPY . /app

# Install Python dependencies specific to the Kafka consumer
RUN pip install --no-cache-dir -r requirements.txt

# Use ARG to pass environment variables at build time
ARG KAFKA_BROKER
ARG POSTGRES_HOST
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_PORT

# Set environment variables in the container
ENV KAFKA_BROKER=$KAFKA_BROKER \
    POSTGRES_HOST=$POSTGRES_HOST \
    POSTGRES_DB=$POSTGRES_DB \
    POSTGRES_USER=$POSTGRES_USER \
    POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    POSTGRES_PORT=$POSTGRES_PORT


# Set permissions for the consumer.py script (if needed)
RUN chmod +x /app/consumer.py

# Define the default command for starting the Kafka consumer
CMD ["python", "consumer.py"]
