import os
import time
from dotenv import load_dotenv
from facebook_scraper import get_posts
import channel

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = os.getenv("FACEBOOK_ID")

# Initialize the Discord Webhook channel
CH = channel.DiscordWebhookChannel(WEBHOOK_URL)

print("Checking for new messages...")

# Fetch the most recent post
try:
    for post in get_posts(FACEBOOK_ID, pages=1):
        post_text = post.get('text', '')
        post_url = post.get('post_url', '')
        
        if post_url:
            message = f"Check out my latest Facebook post: {post_url}"
            CH.send_message(message)
            print("Post sent to Discord successfully!")
            break # Only send the single newest post
except Exception as e:
    print(f"Error fetching Facebook posts: {e}")

print("Check complete. Closing script.")
