# Use OpenJDK as base image
FROM openjdk:11-jdk-slim

# Install Python for integration with Flink jobs
RUN apt-get update && apt-get install -y python3 python3-pip wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Java home and path environment variables
ENV JAVA_HOME /usr/local/openjdk-11
ENV PATH $JAVA_HOME/bin:$PATH

# Install Flink
WORKDIR /opt/flink
RUN wget https://archive.apache.org/dist/flink/flink-1.20.0/flink-1.20.0-bin-scala_2.12.tgz && \
    tar -xzf flink-1.20.0-bin-scala_2.12.tgz && mv flink-1.20.0/* . && rm -rf flink-1.20.0 flink-1.20.0-bin-scala_2.12.tgz

# Copy and install Flink-specific Python dependencies
COPY requirements.txt /opt/flink/requirements.txt
RUN pip3 install --no-cache-dir -r /opt/flink/requirements.txt

# Start the Flink JobManager in foreground
CMD ["bin/jobmanager.sh", "start-foreground"]
