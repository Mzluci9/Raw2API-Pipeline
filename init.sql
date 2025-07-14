-- init.sql
CREATE TABLE stg_telegram_messages (
    id SERIAL PRIMARY KEY,
    message_text TEXT,
    sender_id TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
