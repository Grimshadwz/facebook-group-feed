import os
import base64
from dotenv import load_dotenv
from http.cookiejar import CookieJar, Cookie
from facebook_scraper import get_posts
import channel

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = os.getenv("FACEBOOK_ID")
COOKIE_B64 = os.getenv("FACEBOOK_COOKIES", "")

# 1. Decode the secure Base64 envelope back into a raw string
try:
    decoded_bytes = base64.b64decode(COOKIE_B64)
    COOKIE_RAW = decoded_bytes.decode("utf-8")
except Exception as e:
    print(f"Failed to decode base64 cookies: {e}")
    COOKIE_RAW = ""

# 2. Instantiate a formal native Python CookieJar object
cj = CookieJar()

# 3. Parse and load elements into true Cookie objects to pass internal checks
for item in COOKIE_RAW.split(";"):
    if "=" in item:
        name, val = item.strip().split("=", 1)
        
        # Build the exact programmatic structure the validator demands
        cookie_obj = Cookie(
            version=0, name=name, value=val, port=None, port_specified=False,
            domain=".facebook.com", domain_specified=True, domain_initial_dot=True,
            path="/", path_specified=True, secure=True, expires=None,
            discard=True, comment=None, comment_url=None, rest={}, rfc2109=False
        )
        cj.set_cookie(cookie_obj)

CH = channel.DiscordWebhookChannel(WEBHOOK_URL)
print(f"Checking for new messages on page: {FACEBOOK_ID}...")

try:
    # 4. Pass the formal CookieJar object straight into the parameters
    for post in get_posts(FACEBOOK_ID, pages=1, cookies=cj):
        post_url = post.get('post_url', '')
        if post_url:
            message = f"Check out my latest Facebook post: {post_url}"
            CH.send_message(message)
            print("Post found and sent to Discord successfully!")
            break
except Exception as e:
    print(f"Error fetching Facebook posts: {e}")

print("Check complete.")
