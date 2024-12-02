import io
import logging
from fastavro import writer, reader, parse_schema

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Define the Avro schema
schema = {
    "type": "record",
    "name": "SoccerMatch",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "sport_id", "type": "int"},
        {"name": "league_id", "type": "int"},
        {"name": "season_id", "type": "int"},
        {"name": "stage_id", "type": "int"},
        {"name": "group_id", "type": ["null", "int"], "default": None},
        {"name": "aggregate_id", "type": ["null", "int"], "default": None},
        {"name": "round_id", "type": "int"},
        {"name": "state_id", "type": "int"},
        {"name": "venue_id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "starting_at", "type": ["null", "string"], "default": None},
        {"name": "result_info", "type": ["null", "string"], "default": None},
        {"name": "leg", "type": "string"},
        {"name": "details", "type": ["null", "string"], "default": None},
        {"name": "length", "type": "int"},
        {"name": "placeholder", "type": "boolean"},
        {"name": "has_odds", "type": "boolean"},
        {"name": "has_premium_odds", "type": "boolean"},
        {"name": "starting_at_timestamp", "type": "long"}
    ]
}

parsed_schema = parse_schema(schema)


def serialize_avro(record):
    """Serialize a Python dictionary into Avro bytes."""
    try:
        bytes_writer = io.BytesIO()
        writer(bytes_writer, parsed_schema, [record])
        return bytes_writer.getvalue()
    except Exception as e:
        logging.error(f"Error serializing record: {record}. Exception: {e}")
        raise


def deserialize_avro(message_value):
    """Deserialize Avro bytes into a Python dictionary."""
    try:
        bytes_reader = io.BytesIO(message_value)
        return list(reader(bytes_reader))[0]
    except Exception as e:
        logging.error(f"Error deserializing Avro message. Exception: {e}")
        raise
