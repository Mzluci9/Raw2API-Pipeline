# import os
# import json
# from datetime import datetime
# from telethon.sync import TelegramClient
# from dotenv import load_dotenv

# load_dotenv()

# # Telegram API credentials
# api_id = os.getenv("TELEGRAM_API_ID")
# api_hash = os.getenv("TELEGRAM_API_HASH")

# # Check if credentials are set
# if not api_id or not api_hash:
#     raise ValueError("TELEGRAM_API_ID or TELEGRAM_API_HASH not set in .env")

# # Initialize Telegram client
# client = TelegramClient("session_name", api_id, api_hash)

# async def test_connection():
#     async with client:
#         me = await client.get_me()
#         print(f"Connected as {me.username or me.id}")

# if __name__ == "__main__":
#     client.loop.run_until_complete(test_connection())
    
    
    
    
import os
import json
from datetime import datetime
from pathlib import Path
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()

# Telegram API credentials
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

if not api_id or not api_hash:
    raise ValueError("TELEGRAM_API_ID or TELEGRAM_API_HASH not set in .env")

# Initialize client
client = TelegramClient("session_name", api_id, api_hash)

# Channels to scrape (add more from https://et.tgstat.com/medicine)
CHANNELS = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahpharma",
]

async def scrape_channel(channel_name, limit=100):
    """Scrape messages and images from a Telegram channel."""
    async with client:
        # Ensure data/raw directory exists
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path(f"data/raw/telegram_messages/{date_str}/{channel_name}")
        output_dir.mkdir(parents=True, exist_ok=True)

        messages_data = []
        async for message in client.iter_messages(channel_name, limit=limit):
            msg_data = {
                "id": message.id,
                "date": message.date.isoformat(),
                "text": message.text or "",
                "has_image": bool(message.photo),
            }
            messages_data.append(msg_data)

            # Download images if present
            if message.photo:
                image_path = output_dir / f"image_{message.id}.jpg"
                await message.download_media(file=image_path)

        # Save messages as JSON
        json_path = output_dir / "messages.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)

        print(f"Saved {len(messages_data)} messages to {json_path}")

async def main():
    async with client:
        for channel in CHANNELS:
            print(f"Scraping channel: {channel}")
            await scrape_channel(channel)

if __name__ == "__main__":
    client.loop.run_until_complete(main())