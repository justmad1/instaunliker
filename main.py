import json
from config import TRANSLATION_FILE
from telegram import send_telegram_message
from instagram_client import init_client
from save_db import save_liked_posts_to_db
from unlike import unlike_all_posts, unlike_not_followed_posts, unlike_posts_by_user
from db import init_db, count_posts

def load_translations(lang_code):
    with open(TRANSLATION_FILE, "r", encoding="utf-8") as f:
        all_texts = json.load(f)
        return all_texts.get(lang_code, all_texts["en"])

def main():
    lang_input = input("Choose language / Выберите язык:\n1. English\n2. Русский\n> ").strip()
    LANG = "en" if lang_input == "1" else "ru"
    TEXT = load_translations(LANG)

    send_tg_input = input(TEXT["telegram_prompt"]).strip().lower()
    SEND_TELEGRAM = send_tg_input == "y"

    init_db()

    menu = TEXT["menu"]
    option = input(menu).strip()

    client = init_client()

    if option == "1":
        save_liked_posts_to_db(client, SEND_TELEGRAM, TEXT)
    elif option == "2":
        unlike_all_posts(client, SEND_TELEGRAM, TEXT)
    elif option == "3":
        unlike_not_followed_posts(client, SEND_TELEGRAM, TEXT)
    elif option == "4":
        username = ""
        while not username:
            username = input("username: ").strip()
        unlike_posts_by_user(client, username, SEND_TELEGRAM, TEXT)
    elif option == "5":
        total, followed, not_followed = count_posts()
        stats_msg = TEXT["stats"].format(total=total, followed=followed, not_followed=not_followed)
        print(stats_msg)
        send_telegram_message(stats_msg, SEND_TELEGRAM)
    else:
        print(TEXT["invalid_option"])

if __name__ == "__main__":
    main()