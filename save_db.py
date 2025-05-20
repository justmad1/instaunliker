from db import insert_post
from telegram import send_telegram_message
from db import insert_post
from utils import send_telegram_message

def save_liked_posts_to_db(client, send_telegram, TEXT):
    print("📥 " + TEXT["fetching_liked"])

    liked_posts = client.liked_medias(amount=0)
    print(f"✅ {len(liked_posts)} liked posts fetched.")

    print(TEXT["fetching_users"])
    followed_users = client.user_following(client.user_id)
    followed_ids = set(followed_users.keys())
    print(f"✅ Following {len(followed_ids)} users.")

    saved = 0
    skipped = 0

    for post in liked_posts:
        if post.user is None:
            skipped += 1
            continue

        is_followed = int(post.user.pk in followed_ids)
        insert_post(
            media_id=post.id,
            code=post.code,
            username=post.user.username,
            full_name=post.user.full_name,
            is_followed=is_followed
        )
        saved += 1

    print(f"💾 {saved} posts processed, {skipped} skipped (deleted or no user).")
    send_telegram_message(f"📥 DB filled: {saved} posts saved, {skipped} skipped.", send_telegram)