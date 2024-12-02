# Use Bitnami Spark as the base image
FROM bitnami/spark:3.3.0

# Set the working directory in the container
WORKDIR /app

# Copy and install Spark-specific Python packages
COPY src/spark/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Use the entrypoint script provided by the Bitnami image
ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]
