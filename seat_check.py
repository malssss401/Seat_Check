import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.icaionlineregistration.org/launchbatchdetail.aspx"

PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]


def send_notification(message):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "message": message
        }
    )


session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Step 1: load page
response = session.get(URL, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

# Extract ASP.NET hidden fields
viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]
viewstategen = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]

# Step 2: simulate dropdown selection
payload = {
    "__VIEWSTATE": viewstate,
    "__VIEWSTATEGENERATOR": viewstategen,
    "__EVENTVALIDATION": eventvalidation,
    "ddlRegion": "Southern",
    "ddlPOU": "Chennai",
    "ddlCourse": "AICITSS - Advanced Information Technology",
    "btnSearch": "Search"
}

response = session.post(URL, data=payload, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("tr")

seats_found = 0

for row in rows:
    cols = [c.text.strip() for c in row.find_all("td")]

    for col in cols:
        if col.isdigit():
            seats = int(col)
            seats_found = max(seats_found, seats)

print("Seats detected:", seats_found)

if seats_found > 0:
    send_notification(f"🚨 ICAI Seats Available! {seats_found} seats open.")