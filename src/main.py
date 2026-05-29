import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
INSTAGRAM_USERNAME = "southern_backwoodz"

print(f"Directly querying public timeline layout for: {INSTAGRAM_USERNAME}...")

# Pull directly from Instagram's native public display node instead of a proxy server
url = f"https://instagram.com/{INSTAGRAM_USERNAME}/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    
    # Locate hidden direct shortcode post links inside the script array data
    shortcodes = re.findall(r'"shortcode":"([^"]+)"', response.text)
    
    if shortcodes:
        # Construct the direct web link to your most recent upload item
        latest_shortcode = shortcodes[0]
        full_post_url = f"https://instagram.comp/{latest_shortcode}/"
        print(f"Match found! Direct Link: {full_post_url}")
        
        # Fire the message over to the Discord Webhook directly
        payload = {"content": f"🎨 New update from {INSTAGRAM_USERNAME}! Check out the latest post: {full_post_url}"}
        discord_response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        
        if discord_response.status_code in [200, 204]:
            print("Post found and sent to Discord successfully!")
        else:
            print(f"Discord Webhook rejected request with status: {discord_response.status_code}")
    else:
        # If Instagram serves a dense script block, grab any standard anchor tag extensions
        soup = BeautifulSoup(response.text, 'html.parser')
        found_url = None
        for link in soup.find_all('a', href=True):
            if "/p/" in link['href']:
                found_url = link['href']
                break
                
        if found_url:
            full_post_url = f"https://instagram.com{found_url}"
            payload = {"content": f"🎨 New update from {INSTAGRAM_USERNAME}! Check out the latest post: {full_post_url}"}
            requests.post(WEBHOOK_URL, json=payload, timeout=10)
            print("Post parsed via structural fallback and sent to Discord successfully!")
        else:
            print("No recent timeline updates identified in the current layout view structure.")

except Exception as e:
    print(f"Error executing raw layout transfer check: {e}")

print("Check complete.")
