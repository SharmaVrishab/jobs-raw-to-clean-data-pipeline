import json
import psycopg2
import logging
import os
from src.jobs_pipeline.fetch import fetch_jobs


def get_connection():
    return psycopg2.connect(
        dbname=os.environ.get("PG_DB", "jobs"),
        user=os.environ.get("PG_USER", "postgres"),
        password=os.environ.get("PG_PASSWORD", "postgres"),
        host=os.environ.get("PG_HOST", "localhost"),
        port=os.environ.get("PG_PORT", 5432),
    )


def create_raw_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS raw_jobs (
            id SERIAL PRIMARY KEY,
            ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
            raw_payload JSONB NOT NULL
        );
        """
    )


def insert_raw_jobs():
    logging.info("Starting raw job ingestion")

    data = fetch_jobs()
    logging.info("Fetched job payload")

    conn = get_connection()
    cur = conn.cursor()

    create_raw_table(cur)

    cur.execute(
        "INSERT INTO raw_jobs (raw_payload) VALUES (%s)",
        [json.dumps(data)],
    )

    conn.commit()

    cur.close()
    conn.close()

    logging.info("Raw job ingestion completed")
