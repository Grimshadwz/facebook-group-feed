import os
import json
import base64
from dotenv import load_dotenv
from facebook_scraper import get_posts
import channel

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = os.getenv("FACEBOOK_ID")
COOKIE_B64 = os.getenv("FACEBOOK_COOKIES", "")

# Safely decode the Base64 scramble back into a readable text string
try:
    decoded_bytes = base64.b64decode(COOKIE_B64)
    COOKIE_RAW = decoded_bytes.decode("utf-8")
except Exception as e:
    print(f"Failed to decode base64 cookies: {e}")
    COOKIE_RAW = ""

# Parse the text keys and build a standard JSON Cookie structure
cookies_json_list = []
for item in COOKIE_RAW.split(";"):
    if "=" in item:
        name, val = item.strip().split("=", 1)
        cookies_json_list.append({
            "name": name,
            "value": val,
            "domain": ".facebook.com",
            "path": "/"
        })

# Save the structured cookie list to a local JSON file that the scraper natively accepts
with open("cookies.json", "w") as f:
    json.dump(cookies_json_list, f)

CH = channel.DiscordWebhookChannel(WEBHOOK_URL)
print(f"Checking for new messages on page: {FACEBOOK_ID}...")

try:
    # Pass the local JSON file path directly to bypass validation constraints
    for post in get_posts(FACEBOOK_ID, pages=1, cookies="cookies.json"):
        post_url = post.get('post_url', '')
        if post_url:
            message = f"Check out my latest Facebook post: {post_url}"
            CH.send_message(message)
            print("Post found and sent to Discord successfully!")
            break
except Exception as e:
    print(f"Error fetching Facebook posts: {e}")

# Clean up local system tracking variables
if os.path.exists("cookies.json"):
    os.remove("cookies.json")

print("Check complete.")
