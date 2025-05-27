import time
import random
from datetime import datetime
import os

from telegram import send_telegram_message
from db import get_posts_by_username, unlike_post
from config import *


def log_unliked_post(post):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp},{post['media_id']},{post['username']},{post['full_name']},https://www.instagram.com/p/{post['code']}/\n"
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    with open(STATS_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def unlike_posts_by_user(client, user_name, send_telegram, TEXT):
    posts = get_posts_by_username(user_name)

    if not posts:
        print(TEXT["no_posts_user"].format(username=user_name))
        return

    print(TEXT["start_specific"].format(username=user_name))
    if send_telegram:
        send_telegram_message(TEXT["start_specific"].format(username=user_name), send_telegram)

    count = 0
    block_size = random.randint(*BLOCK_SIZE_RANGE)

    for i, post in enumerate(posts):
        if count >= MAX_UNLIKES_PER_RUN:
            break

        try:
            unlike_post(client, post["media_id"])
            log_unliked_post(post)

            print(TEXT["unliking"].format(id=post["code"], username=user_name))
            count += 1

            time.sleep(random.uniform(*SHORT_PAUSE_RANGE))

            if count % block_size == 0:
                pause_sec = random.uniform(*LONG_PAUSE_RANGE)
                print(TEXT["pause_msg"].format(minutes=pause_sec / 60, count=count))
                time.sleep(pause_sec)
                block_size = random.randint(*BLOCK_SIZE_RANGE)

        except Exception as e:
            print(TEXT["error"].format(error=str(e)))
            continue

    print(TEXT["done"].format(count=count))
    if send_telegram:
        send_telegram_message(TEXT["done"].format(count=count), send_telegram)