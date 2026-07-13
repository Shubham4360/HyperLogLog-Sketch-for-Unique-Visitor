import psycopg2
from psycopg2.extras import RealDictCursor

from config.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)

class PostgreSQL:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            print("Connected successfully!")
        except Exception as e:
            print("Database connection failed:")
            print(e)
            raise
        