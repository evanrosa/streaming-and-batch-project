import logging
import psycopg2
from src.kafka.configs.kafka_client import get_consumer, read_config
import os
from utils.avro_schema import deserialize_avro

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def is_running_in_docker():
    """Check if the script is running inside a Docker container."""
    try:
        with open('/proc/1/cgroup', 'rt') as ifh:
            return 'docker' in ifh.read()
    except FileNotFoundError:
        return False


def insert_into_postgres(data):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "sports"),
            user=os.getenv("POSTGRES_USER", "evro"),
            password=os.getenv("POSTGRES_PASSWORD", "evro"),
            host=os.getenv("POSTGRES_HOST", "sports"),
            port=os.getenv("POSTGRES_PORT", "5432")
        )
        cur = conn.cursor()
        insert_query = """INSERT INTO soccer_matches (
            id, sport_id, league_id, season_id, stage_id, group_id, aggregate_id,
            round_id, state_id, venue_id, name, starting_at, result_info, leg,
            details, length, placeholder, has_odds, has_premium_odds, starting_at_timestamp
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON CONFLICT (id) DO UPDATE SET
            sport_id = EXCLUDED.sport_id,
            league_id = EXCLUDED.league_id,
            season_id = EXCLUDED.season_id,
            stage_id = EXCLUDED.stage_id,
            group_id = EXCLUDED.group_id,
            aggregate_id = EXCLUDED.aggregate_id,
            round_id = EXCLUDED.round_id,
            state_id = EXCLUDED.state_id,
            venue_id = EXCLUDED.venue_id,
            name = EXCLUDED.name,
            starting_at = EXCLUDED.starting_at,
            result_info = EXCLUDED.result_info,
            leg = EXCLUDED.leg,
            details = EXCLUDED.details,
            length = EXCLUDED.length,
            placeholder = EXCLUDED.placeholder,
            has_odds = EXCLUDED.has_odds,
            has_premium_odds = EXCLUDED.has_premium_odds,
            starting_at_timestamp = EXCLUDED.starting_at_timestamp;"""
        values = (
            data["id"], data["sport_id"], data["league_id"], data["season_id"], data["stage_id"],
            data.get("group_id"), data.get("aggregate_id"), data["round_id"], data["state_id"],
            data["venue_id"], data["name"], data.get("starting_at"), data.get("result_info"),
            data["leg"], data.get("details"), data["length"], data["placeholder"], data["has_odds"],
            data["has_premium_odds"], data["starting_at_timestamp"]
        )
        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()
        logging.info(f"Successfully inserted or updated data in PostgreSQL: {data}")
    except Exception as e:
        logging.error(f"Error inserting data into PostgreSQL: {e}")       

def consume_messages(topic, config):
    """Consumes Avro messages from the specified Kafka topic."""
    consumer = get_consumer(config, topic)
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                continue
            try:
                value = deserialize_avro(msg.value())
                logging.info(f"Consumed Avro message: value={value}")
                insert_into_postgres(value)
            except Exception as e:
                logging.error(f"Error deserializing Avro message. Raw message: {msg.value()}. Exception: {e}")
    except KeyboardInterrupt:
        logging.info("Consumer interrupted by user.")
    finally:
        consumer.close()
        logging.info("Consumer closed.")


if __name__ == "__main__":
    LOCAL_CONFIG = os.getenv("LOCAL_CONFIG")

    kafka_config = read_config(file_path=LOCAL_CONFIG)
    topic = "topic_livescores"
    consume_messages(topic, kafka_config)
