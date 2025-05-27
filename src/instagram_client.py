from instagrapi import Client
from pathlib import Path
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, SESSION_FILE


def init_client(TEXT):
    client = Client()
    if Path(SESSION_FILE).exists():
        client.load_settings(SESSION_FILE)
        client.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
    else:
        print(TEXT["session_not_found"])
        client.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
        client.dump_settings(SESSION_FILE)
    return client
