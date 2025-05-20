import sqlite3
import os

DB_FILE = "posts.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                media_id TEXT PRIMARY KEY,
                code TEXT,
                username TEXT,
                full_name TEXT,
                is_followed INTEGER
            )
        """)
        conn.commit()

def insert_post(media_id, code, username, full_name, is_followed):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO posts (media_id, code, username, full_name, is_followed)
            VALUES (?, ?, ?, ?, ?)
        """, (media_id, code, username, full_name, is_followed))
        conn.commit()

def save_posts(posts):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        for post in posts:
            c.execute("""
                INSERT OR IGNORE INTO posts (id, username, is_followed)
                VALUES (?, ?, ?)
            """, (post['id'], post['username'], int(post['is_followed'])))
        conn.commit()

def get_all_posts():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, username FROM posts")
    return [{"id": row[0], "username": row[1]} for row in c.fetchall()]

def count_posts():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM posts")
        total = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM posts WHERE is_followed = 1")
        followed = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM posts WHERE is_followed = 0")
        not_followed = c.fetchone()[0]

    return total, followed, not_followed

def get_not_followed_posts():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, username FROM posts WHERE is_followed = 0")
    return [{"id": row[0], "username": row[1]} for row in c.fetchall()]

def unlike_post(client, post_id):
    client.media_unlike(post_id)

def get_followed_user_ids(client):
    return set(client.user_following(client.user_id).keys())

def get_stats():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM posts")
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM posts WHERE is_followed = 0")
        not_followed = c.fetchone()[0]
    return total, not_followed

def mark_post_unliked(media_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE posts SET is_unliked = 1 WHERE media_id = ?", (media_id,))
        conn.commit()

def get_posts_by_username(username):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT media_id, code FROM posts WHERE username = ? AND is_unliked = 0", (username,))
        rows = c.fetchall()
        return [{"media_id": row[0], "code": row[1]} for row in rows]