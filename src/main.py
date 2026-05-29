import os
import re
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# Hardcoded to absolutely guarantee no string mashing can happen
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = "RatchetArtStudio"
COOKIE_B64 = os.getenv("FACEBOOK_COOKIES", "")

try:
    decoded_bytes = base64.b64decode(COOKIE_B64)
    COOKIE_RAW = decoded_bytes.decode("utf-8")
except Exception:
    COOKIE_RAW = ""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cookie': COOKIE_RAW
}

url = f"https://mbasic.facebook.com/{FACEBOOK_ID}"
print(f"Requesting public page timeline for ID: {FACEBOOK_ID}...")

try:
    response = requests.get(url, headers=headers, timeout=15)
    html_content = response.text
    
    found_url = None
    
    # Sweep for different standard web story layouts
    story_matches = re.findall(r'href="(/story\.php\?[^"]+)"', html_content)
    if story_matches:
        found_url = story_matches[0].replace("&amp;", "&")
    
    if not found_url:
        permalink_matches = re.findall(r'href="(/permalink\.php\?[^"]+)"', html_content)
        if permalink_matches:
            found_url = permalink_matches[0].replace("&amp;", "&")
            
    if not found_url:
        path_matches = re.findall(r'href="(/[^/]+/posts/[^"/?]+)"', html_content)
        if path_matches:
            found_url = path_matches[0]

    if found_url:
        full_post_url = f"https://www.facebook.com{found_url}"
        print(f"Match found! Direct Link: {full_post_url}")
        
        # Fixed syntax conditional evaluation line here
        payload = {"content": f"Check out my latest Facebook post: {full_post_url}"}
        discord_response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        
        if discord_response.status_code in [200, 204]:
            print("Post found and sent to Discord successfully!")
        else:
            print(f"Discord Webhook rejected request with status: {discord_response.status_code}")
    else:
        print("No new recent timeline posts identified in the current layout view.")

except Exception as e:
    print(f"Error executing web transfer check: {e}")

print("Check complete.")
