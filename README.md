# Instagram Unlike Script

This script allows you to **unlike Instagram posts** in bulk using the `instagrapi` Python library.

It can:

- Create a database of all liked posts
- Unlike liked posts by a specific Instagram username
- Send optional Telegram notifications about progress and errors
- Log unliked posts and statistics
- Multilanguage support (English and Russian)

---

## Features

- Efficiently fetches liked posts and creates database to avoid rate limits
- Supports session reuse via saved `session.json`
- Customizable limits and pause intervals to mimic human behavior
- Saves logs and stats into a `logs/` folder
- Translations are stored separately in `lang/translations.json`

---

## Requirements

- Python 3.8+
- [instagrapi](https://github.com/adw0rd/instagrapi)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- `requests` package

---

# Setup

1. Clone or download the repository.
2. Create a .env file in the project root with the following variables:

```bash
TELEGRAM_TOKEN=YOUR_TELEGRAM_TOKEN
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
INSTAGRAM_USERNAME=YOUR_INSTAGRAM_USERNAME
INSTAGRAM_PASSWORD=YOUR_INSTAGRAM_PASSWORD
```

3. Run 'run.sh' on Mac/Linux

```bash
./run.sh
```

or 'run.bat' on Windows

```bash
run.bat
```

Follow the prompts to configure the script.

---

### Configuration Constants

- MAX_UNLIKES_PER_RUN: Max number of unlikes per script run (default 500)
- SHORT_PAUSE_RANGE: Pause time between unlikes in seconds (default 5-10)
- BLOCK_SIZE_RANGE: Number of unlikes between longer pauses (default 80-120)
- LONG_PAUSE_RANGE: Length of long pauses in seconds (default 2700-4500)

### Logs and Stats

- All cache files, logs, and stats are saved inside the `logs/` folder:

---

## Troubleshooting

- Session problems: Delete session.json and log in again.
- For Telegram message failures, verify your bot token and chat ID.

---

# License

MIT License
