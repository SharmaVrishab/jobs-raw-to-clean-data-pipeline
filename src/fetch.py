"""
Main script responsibilities:

- Call the API
- Print response once (optional, debugging)
- Save raw JSON
- Insert raw JSON into Postgres (later stage)

If this file exceeds ~120 lines, it is doing too much.
"""

import json
import requests

URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_jobs():
    """
    Fetch job data from Arbeitnow API.

    Returns:
        dict: Raw JSON response from the API.
    """
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = fetch_jobs()
    #  creating a file here
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)
