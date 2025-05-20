import json
import csv
import time
import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, STATS_FILE


def send_telegram_message(text, send_telegram=True):
    if not send_telegram or not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")


def save_stats(post, timestamp):
    with open(STATS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                timestamp,
                post.id,
                post.user.username if post.user else "",
                post.user.full_name if post.user else "",
                f"https://www.instagram.com/p/{post.code}/",
            ]
        )


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}