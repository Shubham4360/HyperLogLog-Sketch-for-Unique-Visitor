from producer.github_api import GitHubAPI
from producer.kafka_producer import GitHubKafkaProducer
from config.logging_config import setup_logging
from kafka import KafkaProducer



logger = setup_logging()

def main():
    github = GitHubAPI()
    kafka = GitHubKafkaProducer()

    logger.info("GitHub Streaming Producer Started")

    try:
        for event in github.stream_events():
            kafka.send(event)

    except KeyboardInterrupt:
        logger.warning("Stopping producer...")

    finally:
        kafka.close()

if __name__ == "__main__":
    main()