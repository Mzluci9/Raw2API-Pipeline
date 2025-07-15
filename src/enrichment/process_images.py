import os
import json
from pathlib import Path
from ultralytics import YOLO
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "db"),
    port=os.getenv("POSTGRES_PORT", "5432")
)
cursor = conn.cursor()

# Create table for YOLO results
cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_objects (
        id SERIAL PRIMARY KEY,
        message_id INTEGER,
        channel_name VARCHAR,
        image_path VARCHAR,
        object_detected VARCHAR,
        confidence FLOAT
    );
""")
conn.commit()

# Load YOLO model
model = YOLO("yolov8n.pt")  # Pre-trained model

# Process images
data_dir = Path("data/raw/telegram_messages/2025-07-11")
for channel in ["chemed123", "lobelia4cosmetics", "tikvahpharma"]:
    json_path = data_dir / channel / "messages.json"
    with open(json_path, "r") as f:
        messages = json.load(f)
    for msg in messages:
        if msg.get("has_image"):
            image_path = data_dir / channel / f"image_{msg['id']}.jpg"
            if image_path.exists():
                results = model(image_path)
                for result in results:
                    for box in result.boxes:
                        obj_class = result.names[int(box.cls)]
                        confidence = float(box.conf)
                        cursor.execute(
                            """
                            INSERT INTO image_objects (message_id, channel_name, image_path, object_detected, confidence)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (msg["id"], channel, str(image_path), obj_class, confidence)
                        )
                conn.commit()

cursor.close()
conn.close()
print("Image processing complete.")