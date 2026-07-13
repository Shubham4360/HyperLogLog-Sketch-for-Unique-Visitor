from loguru import logger
import sys


def setup_logging():
    logger.remove()

    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time}</green> | <level>{level}</level> | {message}"
    )

    logger.add(
        "logs/application.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO"
    )

    return logger