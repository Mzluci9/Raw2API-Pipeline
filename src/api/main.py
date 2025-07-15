from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Tenx Data Pipeline API")

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

@app.get("/messages/", response_model=list[dict])
async def get_messages(channel_name: str = None, limit: int = 10):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT id, channel_name, message_id, message_text, has_image, object_detected, confidence
            FROM marts.fct_messages_enriched
            WHERE (%s IS NULL OR channel_name = %s)
            LIMIT %s
        """
        cursor.execute(query, (channel_name, channel_name, limit))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if not results:
            raise HTTPException(status_code=404, detail="No messages found")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    