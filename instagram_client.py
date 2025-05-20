from instagrapi import Client
from pathlib import Path
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

def init_client():
    client = Client()
    session_file = "session.json"
    if Path(session_file).exists():
        client.load_settings(session_file)
        client.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
    else:
        print("⚠️ session.json not found. Logging in...")
        client.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
        client.dump_settings(session_file)
    return client