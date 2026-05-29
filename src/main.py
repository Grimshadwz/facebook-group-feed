import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = "RatchetArtStudio"

print(f"Directly checking public web elements for page: {FACEBOOK_ID}...")

# Target the clean profile page structure layout natively
url = f"https://facebook.com{FACEBOOK_ID}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'navigate'
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    html_content = response.text
    
    # Locate tracking numeric Post IDs buried deep inside Facebook's meta tag configurations
    post_ids = re.findall(r'"post_id":"([0-9]+)"', html_content)
    
    if not post_ids:
        # Fallback tracking pattern lookup for standard story layout items
        post_ids = re.findall(r'top_level_post_id\.([0-9]+)', html_content)

    if post_ids:
        # Grab the newest clean numerical identifier found in the code array
        latest_post_id = post_ids[0]
        full_post_url = f"https://facebook.com/{FACEBOOK_ID}/posts/{latest_post_id}"
        print(f"Flawless link generated out of memory: {full_post_url}")
        
        # Dispatch the link string directly over to your Discord server webhook channel
        payload = {"content": f"🎨 New update from RatchetArtStudio! Check it out here: {full_post_url}"}
        discord_response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        
        if discord_response.status_code in [200, 204]:
            print("Update successfully pushed to Discord feed channel!")
        else:
            print(f"Discord Webhook rejected request with status: {discord_response.status_code}")
    else:
        print("No recent timeline updates identified in the current layout cycle.")

except Exception as e:
    print(f"Error executing raw framework check: {e}")

print("Check complete.")
