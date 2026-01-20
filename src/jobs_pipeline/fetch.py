import requests
import logging

URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_jobs():
    """
    Fetch job data from Arbeitnow API.

    Returns:
        dict: Raw JSON response from the API.
    """
    logging.info("Fetching jobs from Arbeitnow API")

    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    logging.info("Jobs fetched successfully")

    return response.json()
