from config.settings import GITHUB_TOKEN

def __init__(self):
    self.headers = {
        "Accept": "application/vnd.github+json"
    }

    if GITHUB_TOKEN:
        self.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    print(self.headers)   # <-- Add this line