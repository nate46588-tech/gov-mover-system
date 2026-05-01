import requests
from datetime import datetime, timedelta

def fetch_awards():
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"

    today = datetime.utcnow().date()
    last_week = today - timedelta(days=7)

    payload = {
        "filters": {
            "time_period": [{
                "start_date": last_week.strftime("%Y-%m-%d"),
                "end_date": today.strftime("%Y-%m-%d")
            }]
        },
        "fields": ["Recipient Name", "Award Amount"],
        "limit": 100
    }

    r = requests.post(url, json=payload).json()
    return r.get("results", [])
