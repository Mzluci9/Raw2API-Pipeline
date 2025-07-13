import os
import json
from pathlib import Path
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# PostgreSQL connection
conn_params = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
}

def create_raw_table():
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS raw_messages (
                    id SERIAL PRIMARY KEY,
                    channel_name VARCHAR,
                    message_id INTEGER,
                    message_date TIMESTAMP,
                    message_text TEXT,
                    has_image BOOLEAN,
                    raw_json JSONB
                );
            """)
            conn.commit()
            print("Created raw_messages table")

def load_json_to_postgres(json_path, channel_name):
    with open(json_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            for msg in messages:
                cur.execute("""
                    INSERT INTO raw_messages (channel_name, message_id, message_date, message_text, has_image, raw_json)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    channel_name,
                    msg["id"],
                    msg["date"],
                    msg["text"],
                    msg["has_image"],
                    json.dumps(msg)
                ))
            conn.commit()
            print(f"Loaded {len(messages)} messages from {channel_name} to PostgreSQL")

if __name__ == "__main__":
    date_str = datetime.now().strftime("%Y-%m-%d")
    data_dir = Path(f"data/raw/telegram_messages/{date_str}")
    create_raw_table()
    for channel in ["chemed123", "lobelia4cosmetics", "tikvahpharma"]:
        json_path = data_dir / channel / "messages.json"
        if json_path.exists():
            load_json_to_postgres(json_path, channel)
        else:
            print(f"No data found for {channel}")