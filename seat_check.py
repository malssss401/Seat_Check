import requests
from bs4 import BeautifulSoup
import os
import json
from pathlib import Path

URL = "https://www.icaionlineregistration.org/launchbatchdetail.aspx"

PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]

STATE_FILE = "seat_state.json"


def send_notification(message):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "message": message
        }
    )


def load_previous_state():
    if Path(STATE_FILE).exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"alert_sent": False}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def check_seats():

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr")

    seats_found = 0

    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]

        for col in cols:
            if col.isdigit():
                seats = int(col)
                seats_found = max(seats_found, seats)

    return seats_found


if __name__ == "__main__":

    state = load_previous_state()
    seats = check_seats()

    print(f"Seats detected: {seats}")

    if seats > 0 and not state["alert_sent"]:
        send_notification(f"🚨 ICAI seats available! {seats} seats open.")
        state["alert_sent"] = True
        save_state(state)
        print("Notification sent.")

    elif seats == 0:
        state["alert_sent"] = False
        save_state(state)
        print("No seats available.")

    else:
        print("Seats already notified earlier.")
