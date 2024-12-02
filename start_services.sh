#!/bin/bash
python3 src/ingestion/message_producer.py &
python3 src/ingestion/message_consumer.py