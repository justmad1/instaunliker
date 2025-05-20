import time
import random
from utils import send_telegram_message
from db import get_all_posts, get_not_followed_posts, unlike_post, get_posts_by_username, mark_post_unliked
from utils import send_telegram_message
from config import *

def unlike_all_posts(client, send_telegram):
    posts = get_all_posts()
    if not posts:
        print("DB is empty. Please fill the database first.")
        if send_telegram:
            send_telegram_message("DB is empty. Please fill the database first.")
        return

    count = 0
    block_limit = random.randint(*BLOCK_SIZE_RANGE)

    for post in posts:
        if count >= MAX_UNLIKES_PER_RUN:
            break
        try:
            unlike_post(client, post)
            count += 1
            print(f"Unliked post {post['id']} by @{post['username']}")
            time.sleep(random.uniform(*SHORT_PAUSE_RANGE))

            if count % block_limit == 0 and count < MAX_UNLIKES_PER_RUN:
                long_pause = random.uniform(*LONG_PAUSE_RANGE)
                msg = f"Pause for {round(long_pause/60,1)} minutes after {count} unlikes."
                print(msg)
                if send_telegram:
                    send_telegram_message(msg)
                time.sleep(long_pause)
                block_limit = random.randint(*BLOCK_SIZE_RANGE)
        except Exception as e:
            err_msg = f"Error during unlike: {str(e)}"
            print(err_msg)
            if send_telegram:
                send_telegram_message(err_msg)
            break
    done_msg = f"Done! Unliked {count} posts."
    print(done_msg)
    if send_telegram:
        send_telegram_message(done_msg)

def unlike_not_followed_posts(client, send_telegram, TEXT):
    posts = get_not_followed_posts()
    if not posts:
        print(TEXT["db_empty"])
        if send_telegram:
            send_telegram_message("DB is empty or no posts from unfollowed users. Please fill the database first.")
        return

    count = 0
    block_limit = random.randint(*BLOCK_SIZE_RANGE)

    for post in posts:
        if count >= MAX_UNLIKES_PER_RUN:
            break
        try:
            unlike_post(client, post)
            count += 1
            print(f"Unliked post {post['id']} by @{post['username']}")
            time.sleep(random.uniform(*SHORT_PAUSE_RANGE))

            if count % block_limit == 0 and count < MAX_UNLIKES_PER_RUN:
                long_pause = random.uniform(*LONG_PAUSE_RANGE)
                msg = f"Pause for {round(long_pause/60,1)} minutes after {count} unlikes."
                print(msg)
                if send_telegram:
                    send_telegram_message(msg)
                time.sleep(long_pause)
                block_limit = random.randint(*BLOCK_SIZE_RANGE)
        except Exception as e:
            err_msg = f"Error during unlike: {str(e)}"
            print(err_msg)
            if send_telegram:
                send_telegram_message(err_msg)
            break
    done_msg = f"Done! Unliked {count} posts."
    print(done_msg)
    if send_telegram:
        send_telegram_message(done_msg)

def unlike_posts_by_user(client, user_name, send_telegram, TEXT):
    posts = get_posts_by_username(user_name)
    if not posts:
        print(TEXT["no_posts_user"].format(username=user_name))
        return

    print(TEXT["start_specific"].format(username=user_name))
    if send_telegram:
        send_telegram_message(TEXT["start_specific"].format(username=user_name))

    count = 0
    block_size = random.randint(*BLOCK_SIZE_RANGE)

    for i, post in enumerate(posts):
        if count >= MAX_UNLIKES_PER_RUN:
            break

        try:
            client.media_unlike(post["media_id"])
            mark_post_unliked(post["media_id"])
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
        send_telegram_message(TEXT["done"].format(count=count))