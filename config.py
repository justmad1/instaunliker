import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

MAX_UNLIKES_PER_RUN = 500
SHORT_PAUSE_RANGE = (5, 10)
BLOCK_SIZE_RANGE = (80, 120)
LONG_PAUSE_RANGE = (45 * 60, 75 * 60)

DB_FILE = "insta_likes.db"
TRANSLATION_FILE = "translations.json"
STATS_FILE = "logs/unliked_stats.csv"