import psycopg2
from psycopg2.extras import RealDictCursor

from config.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
)


class PostgreSQL:

    def __init__(self):
        self.connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )

    def insert_metrics(
        self,
        events_processed,
        exact_users,
        hll_users,
        error_percentage,
        memory_usage_bytes,
    ):

        query = """
        INSERT INTO stream_metrics (
            events_processed,
            exact_users,
            hll_users,
            error_percentage,
            memory_usage_bytes
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(
                query,
                (
                    events_processed,
                    exact_users,
                    hll_users,
                    error_percentage,
                    memory_usage_bytes,
                ),
            )

            self.connection.commit()

        except Exception as e:
            print("Database Insert Error:", e)
            self.connection.rollback()

        finally:
            cursor.close()

    def fetch_latest(self, limit=100):

        cursor = self.connection.cursor(cursor_factory=RealDictCursor)

        try:

            query = """
            SELECT *
            FROM stream_metrics
            ORDER BY timestamp DESC
            LIMIT %s
            """

            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

            # Return oldest -> newest
            return list(reversed(rows))

        except Exception as e:
            print("Database Fetch Error:", e)
            return []

        finally:
            cursor.close()

    def close(self):
        self.connection.close()
