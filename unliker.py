import os
import time
import json
import random
import csv
import requests
from pathlib import Path
from instagrapi import Client
from dotenv import load_dotenv

# ============ CONFIG =============

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

MAX_UNLIKES_PER_RUN = 500
SHORT_PAUSE_RANGE = (10, 20)
BLOCK_SIZE_RANGE = (80, 120)
LONG_PAUSE_RANGE = (45 * 60, 75 * 60)

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LIKED_CACHE_FILE = os.path.join(LOGS_DIR, "liked_cache.json")
UNLIKED_LOG_FILE = os.path.join(LOGS_DIR, "unliked_log.json")
STATS_FILE = os.path.join(LOGS_DIR, "unliked_stats.csv")
TRANSLATION_FILE = "translations.json"

# ============ I18N SETUP =============

def load_translations(lang_code):
    with open(TRANSLATION_FILE, "r", encoding="utf-8") as f:
        all_texts = json.load(f)
        return all_texts.get(lang_code, all_texts["en"])

lang_input = input("Choose language / Выберите язык:\n1. English\n2. Русский\n> ").strip()
LANG = "en" if lang_input == "1" else "ru"
TEXT = load_translations(LANG)

send_tg_input = input(TEXT["telegram_prompt"]).strip().lower()
SEND_TELEGRAM = send_tg_input == "y"

mode_input = input(TEXT["unlike_mode"]).strip()
UNLIKE_MODE = mode_input
TARGET_USERNAME = ""
if UNLIKE_MODE == "3":
    TARGET_USERNAME = input(TEXT["enter_username"]).strip()

    if not TARGET_USERNAME:
        print(TEXT.get("missing_username", "Username required. Exiting."))
        exit(1)

# ============ TELEGRAM =============

def send_telegram_message(text):
    if not SEND_TELEGRAM or not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

# ============ INIT CLIENT =============

def init_client():
    client = Client()
    session_file = "session.json"

    if Path(session_file).exists():
        client.load_settings(session_file)
        client.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
    else:
        print(TEXT.get("session_missing", "⚠️ session.json not found. Logging in..."))
        client.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
        client.dump_settings(session_file)

    return client

# ============ HELPERS =============

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f)

def load_json(path):
    if Path(path).exists():
        with open(path) as f:
            return json.load(f)
    return {}

def save_stats(post, timestamp):
    with open(STATS_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            post.id,
            post.user.username if post.user else "",
            post.user.full_name if post.user else "",
            f"https://www.instagram.com/p/{post.code}/"
        ])

# ============ MAIN UNLIKE FUNCTIONS =============

def iter_liked_medias(client, batch_size=100, max_total=500):
    """Yield liked medias in chunks of `batch_size` up to `max_total` total"""
    all_ids = set()
    fetched = 0

    while fetched < max_total:
        batch = client.liked_medias(amount=batch_size)
        new_batch = [m for m in batch if m.id not in all_ids]

        if not new_batch:
            break

        for m in new_batch:
            all_ids.add(m.id)

        yield new_batch
        fetched += len(new_batch)
        time.sleep(random.uniform(1, 3))

def unlike_liked_posts(client):
    send_telegram_message(TEXT["start"])

    print(TEXT["fetching"])
    followed_users = client.user_following(client.user_id)
    followed_ids = set(followed_users.keys())

    if Path(LIKED_CACHE_FILE).exists():
        liked = [client.media_info(mid) for mid in load_json(LIKED_CACHE_FILE)]
    else:
        liked = []
        for chunk in iter_liked_medias(client, batch_size=100, max_total=1000):
            liked.extend(chunk)
        save_json([m.id for m in liked], LIKED_CACHE_FILE)

    unliked_ids = set(load_json(UNLIKED_LOG_FILE))

    count = 0
    block_limit = random.randint(*BLOCK_SIZE_RANGE)
    print(f"{TEXT['start']} Max: {MAX_UNLIKES_PER_RUN}")

    for post in liked:
        if post.id in unliked_ids:
            continue

        if UNLIKE_MODE == "1" and (not post.user or post.user.pk in followed_ids):
            continue

        try:
            client.media_unlike(post.id)
            unliked_ids.add(post.id)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            save_stats(post, timestamp)

            count += 1
            print(TEXT["unliking"].format(id=post.id, username=post.user.username if post.user else ""))
            time.sleep(random.uniform(*SHORT_PAUSE_RANGE))

            if count % block_limit == 0 and count < MAX_UNLIKES_PER_RUN:
                long_pause = random.uniform(*LONG_PAUSE_RANGE)
                msg = TEXT["pause_msg"].format(minutes=round(long_pause / 60, 1), count=count)
                print(msg)
                send_telegram_message(msg)
                time.sleep(long_pause)
                block_limit = random.randint(*BLOCK_SIZE_RANGE)

            if count >= MAX_UNLIKES_PER_RUN:
                break

        except Exception as e:
            err_msg = TEXT["error"].format(error=str(e))
            print(err_msg)
            send_telegram_message(err_msg)
            break

    save_json(list(unliked_ids), UNLIKED_LOG_FILE)
    final_msg = TEXT["done"].format(count=count)
    print(final_msg)
    send_telegram_message(final_msg)

def unlike_user_posts(client, username):
    send_telegram_message(TEXT["start_specific"].format(username=username))

    unliked_ids = set(load_json(UNLIKED_LOG_FILE))
    count = 0
    block_limit = random.randint(*BLOCK_SIZE_RANGE)

    print(f"Fetching liked posts...")
    for chunk in iter_liked_medias(client, batch_size=100, max_total=1000):
        for post in chunk:
            if post.id in unliked_ids:
                continue

            if not post.user or post.user.username.lower() != username.lower():
                continue

            try:
                client.media_unlike(post.id)
                unliked_ids.add(post.id)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                save_stats(post, timestamp)

                count += 1
                print(TEXT["unliking"].format(id=post.id, username=username))
                time.sleep(random.uniform(*SHORT_PAUSE_RANGE))

                if count % block_limit == 0 and count < MAX_UNLIKES_PER_RUN:
                    long_pause = random.uniform(*LONG_PAUSE_RANGE)
                    msg = TEXT["pause_msg"].format(minutes=long_pause / 60, count=count)
                    print(msg)
                    send_telegram_message(msg)
                    time.sleep(long_pause)
                    block_limit = random.randint(*BLOCK_SIZE_RANGE)

                if count >= MAX_UNLIKES_PER_RUN:
                    raise StopIteration()

            except StopIteration:
                break
            except Exception as e:
                err_msg = TEXT["error"].format(error=str(e))
                print(err_msg)
                send_telegram_message(err_msg)
                break

    save_json(list(unliked_ids), UNLIKED_LOG_FILE)
    msg = TEXT["done"].format(count=count)
    print(msg)
    send_telegram_message(msg)

# ============ ENTRY POINT =============

if __name__ == "__main__":
    client = init_client()

    if UNLIKE_MODE == "3":
        unlike_user_posts(client, TARGET_USERNAME)
    else:
        unlike_liked_posts(client)