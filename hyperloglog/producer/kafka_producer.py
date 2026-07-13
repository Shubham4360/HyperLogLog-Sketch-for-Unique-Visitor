import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
from loguru import logger

from config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


class GitHubKafkaProducer:

    def __init__(self):
        self.topic = KAFKA_TOPIC
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            retries=5
        )
        logger.info("Kafka Producer Connected")

    def send(self, data):
        try:
            self.producer.send(self.topic, value=data)
            logger.info(f"Sent event {data['event_id']}")
        except KafkaError as e:
            logger.error(f"Kafka error: {e}")

    def close(self):
        self.producer.flush()
        self.producer.close()