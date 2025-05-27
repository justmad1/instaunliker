import os
import json
from config import TRANSLATION_FILE, DB_FILE
from instagram_client import init_client
from unlike import unlike_posts_by_user
from db import init_db
from save_db import save_liked_posts_to_db


def load_translations(lang_code):
    with open(TRANSLATION_FILE, "r", encoding="utf-8") as f:
        all_texts = json.load(f)
        return all_texts.get(lang_code, all_texts["en"])


def main():
    lang_input = input(
        "Choose language / Выберите язык:\n1. English\n2. Русский\n> "
    ).strip()
    LANG = "en" if lang_input == "1" else "ru"
    TEXT = load_translations(LANG)

    send_tg_input = input(TEXT["telegram_prompt"]).strip().lower()
    SEND_TELEGRAM = send_tg_input == "y"

    client = init_client(TEXT)

    if not os.path.exists(DB_FILE):
        print(TEXT["creating_db"])
        init_db()
        save_liked_posts_to_db(client, SEND_TELEGRAM, TEXT)
        print(TEXT["db_created"])
    else:
        print(TEXT["db_exists"])

    username = ""
    while not username:
        username = input(TEXT["enter_username"]).strip()

    unlike_posts_by_user(client, username, SEND_TELEGRAM, TEXT)


if __name__ == "__main__":
    main()
