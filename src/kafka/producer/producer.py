import os
import random
import time
import logging
from src.kafka.configs.kafka_client import get_producer, read_config
from utils.avro_schema import serialize_avro

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def produce_message(topic, config, key, value):
    """Produces an Avro message to the specified Kafka topic."""
    producer = get_producer(config)
    try:
        avro_value = serialize_avro(value)
        producer.produce(topic, key=str(key), value=avro_value)
        producer.flush()
        logging.info(f"Produced Avro message to topic {topic}: key={key}, value={value}")
    except Exception as e:
        logging.error(f"Error producing message to topic {topic}. Key: {key}, Value: {value}. Exception: {e}")


if __name__ == "__main__":
    LOCAL_CONFIG = os.getenv("LOCAL_CONFIG")

    kafka_config = read_config(file_path=LOCAL_CONFIG)
    topic = "topic_livescores"

    # Example test message
    test_message = {
        "id": 1,
        "sport_id": 1,
        "league_id": 123,
        "season_id": 2023,
        "stage_id": 456,
        "group_id": None,
        "aggregate_id": None,
        "round_id": 1,
        "state_id": 1,
        "venue_id": 1001,
        "name": "Test Match",
        "starting_at": None,
        "result_info": None,
        "leg": "first",
        "details": None,
        "length": 90,
        "placeholder": False,
        "has_odds": True,
        "has_premium_odds": False,
        "starting_at_timestamp": int(time.time())
    }

    for i in range(10):
        test_message["id"] = i
        test_message["name"] = f"Match {i}"
        test_message["starting_at_timestamp"] = int(time.time()) + random.randint(0, 3600)
        produce_message(topic, kafka_config, key=test_message["id"], value=test_message)
        time.sleep(1)
