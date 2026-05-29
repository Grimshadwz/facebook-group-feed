import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
# Enter your exact Instagram account name here
INSTAGRAM_USERNAME = "southern_backwoodz" 

print(f"Requesting public timeline feed for username: {INSTAGRAM_USERNAME}...")

# Connect to a permanent, unblocked public RSS mirror framework
url = f"https://tinfoil-hat.net{INSTAGRAM_USERNAME}"

try:
    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.text, 'xml')
    
    # Locate the most recent data entry block on your timeline
    item = soup.find('item')
    
    if item:
        link_element = item.find('link')
        if link_element:
            insta_url = link_element.text.strip()
            print(f"Match successfully generated: {insta_url}")
            
            # Construct a clean message text payload to forward out
            message_content = f"🎨 New update from RatchetArtStudio! Check out the latest post: {insta_url}"
            
            payload = {"content": message_content}
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
    print(f"Error executing bridge transfer check: {e}")

print("Check complete.")
