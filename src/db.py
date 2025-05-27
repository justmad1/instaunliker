import sqlite3
from config import DB_FILE


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                media_id TEXT PRIMARY KEY,
                code TEXT,
                username TEXT,
                full_name TEXT,
                is_followed INTEGER
                is_unliked INTEGER
            )
        """
        )
        conn.commit()


def insert_post(media_id, code, username, full_name, is_followed):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            """
            INSERT OR IGNORE INTO posts (media_id, code, username, full_name, is_followed, is_unliked)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (media_id, code, username, full_name, is_followed, 0),
        )
        conn.commit()


def unlike_post(client, media_id):
    client.media_unlike(media_id)

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE posts SET is_unliked = 1 WHERE media_id = ?", (media_id,))
        conn.commit()


def get_posts_by_username(username):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM posts WHERE username = ? AND is_unliked = 0",
            (username,),
        )
        rows = c.fetchall()

        return [
            {
                "media_id": row[0],
                "code": row[1],
                "username": row[2],
                "full_name": row[3],
                "is_followed": row[4],
            }
            for row in rows
        ]
