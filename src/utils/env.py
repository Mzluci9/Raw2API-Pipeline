import os
from dotenv import load_dotenv

load_dotenv()

def get_env_vars():
    env_vars = {
        "TELEGRAM_API_ID": os.getenv("TELEGRAM_API_ID"),
        "TELEGRAM_API_HASH": os.getenv("TELEGRAM_API_HASH"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB"),
    }
    for key, value in env_vars.items():
        print(f"{key}: {'Set' if value else 'Not set'}")

if __name__ == "__main__":
    get_env_vars()