import requests
import os
from datetime import datetime

PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]

message = f"✅ GitHub seat monitor test ran successfully at {datetime.utcnow()}"

requests.post(
    "https://api.pushover.net/1/messages.json",
    data={
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": message
    }
)

print("Notification sent.")
