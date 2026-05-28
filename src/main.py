import os
import re
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = os.getenv("FACEBOOK_ID")
COOKIE_B64 = os.getenv("FACEBOOK_COOKIES", "")

# 1. Decode the Base64 cookie string back to plain text
try:
    decoded_bytes = base64.b64decode(COOKIE_B64)
    COOKIE_RAW = decoded_bytes.decode("utf-8")
except Exception:
    COOKIE_RAW = ""

# 2. Build standard, direct headers for the browser session request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cookie': COOKIE_RAW
}

print(f"Requesting public page timeline for: {FACEBOOK_ID}...")

# 3. Pull raw HTML text directly from the target mobile web layout
url = f"https://mbasic.facebook.com/{FACEBOOK_ID}"

try:
    response = requests.get(url, headers=headers, timeout=15)
    html_content = response.text
    
    # 4. Extract story tracking links using an exact regex string match pattern
    post_matches = re.findall(r'href="(/story\.php\?[^"]+)"', html_content)
    
    if post_matches:
        # Construct the first clean direct URL address match found on the layout
        clean_path = post_matches[0].replace("&amp;", "&")
        full_post_url = f"https://www.facebook.com{clean_path}"
        
        # 5. Push the constructed post link payload over to the Discord Webhook URL directly
        payload = {"content": f"Check out my latest Facebook post: {full_post_url}"}
        discord_response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        
        if discord_response.status_code in [200, 204]:
            print("Post found and sent to Discord successfully!")
        else:
            print(f"Discord Webhook rejected request with status: {discord_response.status_code}")
    else:
        print("No new recent timeline posts identified in this loop cycle.")

except Exception as e:
    print(f"Error executing web transfer check: {e}")

print("Check complete.")
