import os
import base64
from dotenv import load_dotenv
from facebook_scraper import get_posts
import channel

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = os.getenv("FACEBOOK_ID")
COOKIE_B64 = os.getenv("FACEBOOK_COOKIES", "")

# 1. Safely decode the Base64 scramble back into a raw text string
try:
    decoded_bytes = base64.b64decode(COOKIE_B64)
    COOKIE_RAW = decoded_bytes.decode("utf-8")
except Exception as e:
    print(f"Failed to decode base64 cookies: {e}")
    COOKIE_RAW = ""

# 2. Parse the pure string keys straight into an active memory dictionary
cookie_dict = {}
for item in COOKIE_RAW.split(";"):
    if "=" in item:
        name, val = item.strip().split("=", 1)
        cookie_dict[name] = val

CH = channel.DiscordWebhookChannel(WEBHOOK_URL)
print(f"Checking for new messages on page: {FACEBOOK_ID}...")

try:
    # 3. Pass the actual object variable directly so it skips file type checking rules
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
