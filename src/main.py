import os
from dotenv import load_dotenv
from facebook_scraper import get_posts
import channel

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = os.getenv("FACEBOOK_ID")
COOKIE_RAW = os.getenv("FACEBOOK_COOKIES", "")

# Parse the semicolon string manually into the proper Netscape file layout the library requires
cookie_lines = [
    "# Netscape HTTP Cookie File",
    "# http://haxx.se",
    "# This is a generated file! Do not edit.",
    ""
]

# Break the string up by semicolons and build clean data rows
for item in COOKIE_RAW.split(";"):
    if "=" in item:
        name, val = item.strip().split("=", 1)
        # Format: domain, include_subdomains, path, secure, expiry, name, value
        cookie_lines.append(f".facebook.com\tTRUE\t/\tTRUE\t0\t{name}\t{val}")

# Write the formatted output out to cookies.txt
with open("cookies.txt", "w") as f:
    f.write("\n".join(cookie_lines) + "\n")

CH = channel.DiscordWebhookChannel(WEBHOOK_URL)
print(f"Checking for new messages on page: {FACEBOOK_ID}...")

try:
    # Run the scraper with our newly formatted file layout
    for post in get_posts(FACEBOOK_ID, pages=1, cookies="cookies.txt"):
        post_url = post.get('post_url', '')
        if post_url:
            message = f"Check out my latest Facebook post: {post_url}"
            CH.send_message(message)
            print("Post found and sent to Discord successfully!")
            break
except Exception as e:
    print(f"Error fetching Facebook posts: {e}")

# Clean up security variables
if os.path.exists("cookies.txt"):
    os.remove("cookies.txt")

print("Check complete.")
