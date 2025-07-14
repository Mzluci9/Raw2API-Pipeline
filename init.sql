-- init.sql
CREATE TABLE IF NOT EXISTS raw_messages (
    id SERIAL PRIMARY KEY,
    channel_name VARCHAR,
    message_id INTEGER,
    message_date TIMESTAMP,
    message_text TEXT,
    has_image BOOLEAN,
    raw_json JSONB
);