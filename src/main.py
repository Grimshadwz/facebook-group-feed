import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = "RatchetArtStudio"

print(f"Requesting clean open-source timeline tracking for: {FACEBOOK_ID}...")

# Connect directly to the community-maintained free RSSHub database node
url = f"https://rsshub.app{FACEBOOK_ID}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'xml') # Read native XML data nodes
    
    # Isolate the newest timeline post element
    item = soup.find('item')
    
    if item:
        link_element = item.find('link')
        if link_element:
            full_post_url = link_element.text.strip()
            print(f"Match successfully generated: {full_post_url}")
            
            # Forward the clean link straight to your Discord server webhook
            payload = {"content": f"🎨 New update from RatchetArtStudio! Check it out here: {full_post_url}"}
            discord_response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
            
            if discord_response.status_code in [200, 204]:
                print("Update successfully pushed to Discord channel feed!")
            else:
                print(f"Discord Webhook rejected request with status: {discord_response.status_code}")
        else:
            print("Link property data missing from target node structure.")
    else:
        print("No recent timeline updates identified in the current layout cycle.")

except Exception as e:
    print(f"Error executing community network check: {e}")

print("Check complete.")
