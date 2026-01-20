import json
import psycopg2
from fetch import fetch_jobs


def insert_raw_jobs():
    conn = psycopg2.connect(
        dbname="jobs",
        user="postgres",
        password="postgres",
        host="localhost"
    )

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS raw_jobs (
            id SERIAL PRIMARY KEY,
            ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
            raw_payload JSONB NOT NULL
        );
        """
    )

    data = fetch_jobs()


    #  data is transfering in string / bytes not as python object so we need to make it json string

    cur.execute(
        "INSERT INTO raw_jobs (raw_payload) VALUES (%s)", [json.dumps(data)]
    )

    conn.commit()

    cur.close()
    conn.close()


def print_rows():
    conn = psycopg2.connect(
        dbname="jobs",
        user="postgres",
        password="postgres",
        host="localhost"
    )

    cur = conn.cursor()
    cur.execute("SELECT id, ingested_at, raw_payload FROM raw_jobs")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    insert_raw_jobs()
    print_rows()
