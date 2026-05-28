import os
from dotenv import load_dotenv
from facebook_scraper import get_posts
import channel

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = os.getenv("FACEBOOK_ID")
COOKIE_TXT = os.getenv("FACEBOOK_COOKIES")

# Write the cookie string to a temporary file for the scraper to use
with open("cookies.txt", "w") as f:
    f.write(COOKIE_TXT if COOKIE_TXT else "")

CH = channel.DiscordWebhookChannel(WEBHOOK_URL)
print(f"Checking for new messages on page: {FACEBOOK_ID}...")

try:
    # Added cookies='cookies.txt' to bypass Meta blocks
    for post in get_posts(FACEBOOK_ID, pages=1, cookies="cookies.txt"):
        post_url = post.get('post_url', '')
        if post_url:
            message = f"Check out my latest Facebook post: {post_url}"
            CH.send_message(message)
            print("Post found and sent to Discord successfully!")
            break
except Exception as e:
    print(f"Error fetching Facebook posts: {e}")

# Clean up the cookie file
if os.path.exists("cookies.txt"):
    os.remove("cookies.txt")

print("Check complete.")
