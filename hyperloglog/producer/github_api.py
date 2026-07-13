import time
import requests

from loguru import logger

from config.settings import GITHUB_TOKEN, POLL_INTERVAL


class GitHubAPI:

    BASE_URL = "https://api.github.com/events"

    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github+json"
        }

        if GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    def get_events(self):
        retries = 3

        for attempt in range(retries):
            try:
                response = requests.get(
                    self.BASE_URL,
                    headers=self.headers,
                    timeout=20
                )

                response.raise_for_status()
                return response.json()

            except Exception as e:
                logger.error(f"GitHub API error: {e}")
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time}s")
                time.sleep(wait_time)

        return []

    def stream_events(self):
        processed_ids = set()

        while True:
            events = self.get_events()

            for event in events:
                event_id = event.get("id")

                if event_id in processed_ids:
                    continue

                processed_ids.add(event_id)

                yield {
                    "event_id": event_id,
                    "event_type": event.get("type"),
                    "user_id": str(
                        event.get("actor", {}).get("id")
                    ),
                    "username": event.get("actor", {}).get("login"),
                    "repo": event.get("repo", {}).get("name"),
                    "created_at": event.get("created_at")
                }

            time.sleep(POLL_INTERVAL)