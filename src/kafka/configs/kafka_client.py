import logging
import os
from confluent_kafka import Producer, Consumer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

LOCAL_CONFIG = os.getenv("LOCAL_CONFIG")


def read_config(file_path=LOCAL_CONFIG):
    """Reads the Kafka client configuration from a properties file."""
    config = {}
    try:
        with open(file_path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("["):
                    continue
                if '=' not in line:
                    logging.warning(f"Skipping invalid config line: {line}")
                    continue
                parameter, value = line.split('=', 1)
                config[parameter.strip()] = value.strip()
    except FileNotFoundError:
        logging.error(f"Configuration file not found at {file_path}.")
    return config


def get_producer(config):
    """Initialize a Kafka producer."""
    print(
        'producer'
    )
    return Producer(config)


def get_consumer(config, topic):
    """Initialize a Kafka consumer."""
    config["group.id"] = "python-group-1"
    config["auto.offset.reset"] = "earliest"
    consumer = Consumer(config)
    consumer.subscribe([topic])
    return consumer
