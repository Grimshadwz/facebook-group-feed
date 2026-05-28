import os
from dotenv import load_dotenv
from facebook_scraper import get_posts
import channel

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = os.getenv("FACEBOOK_ID")
COOKIE_RAW = os.getenv("FACEBOOK_COOKIES", "")

# Build a clean dictionary directly out of the raw text string
cookie_dict = {}
for item in COOKIE_RAW.split(";"):
    if "=" in item:
        name, val = item.strip().split("=", 1)
        cookie_dict[name] = val

CH = channel.DiscordWebhookChannel(WEBHOOK_URL)
print(f"Checking for new messages on page: {FACEBOOK_ID}...")

try:
    # Pass the clean dictionary directly into the cookies argument
    for post in get_posts(FACEBOOK_ID, pages=1, cookies=cookie_dict):
        post_url = post.get('post_url', '')
        if post_url:
            message = f"Check out my latest Facebook post: {post_url}"
            CH.send_message(message)
            print("Post found and sent to Discord successfully!")
            break
except Exception as e:
    print(f"Error fetching Facebook posts: {e}")

print("Check complete.")
