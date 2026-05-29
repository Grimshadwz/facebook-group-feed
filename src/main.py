import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
FACEBOOK_ID = "RatchetArtStudio"

print(f"Querying official public platform nodes for ID: {FACEBOOK_ID}...")

# Target Meta's unblocked public metadata tracking layer directly
url = f"https://facebook.com/{FACEBOOK_ID}/posts"

try:
    # Requests the public data feed natively without requiring a browser session layout
    response = requests.get(url, timeout=15)
    data = response.json()
    
    if "data" in data and len(data["data"]) > 0:
        # Grab the newest published timeline element from the payload array
        latest_post = data["data"][0]
        post_id = latest_post.get("id")
        
        if post_id:
            # Reconstruct the flawless direct desktop link to your business update
            # The ID comes in as PageID_PostID, we split to get the clean post string
            clean_post_id = post_id.split("_")[-1]
            full_post_url = f"https://www.facebook.com/{FACEBOOK_ID}/posts/{clean_post_id}"
            
            print(f"Match successfully generated: {full_post_url}")
            
            # Pipe the link right over to your Discord Webhook address
            payload = {"content": f"Check out my latest Facebook post: {full_post_url}"}
            discord_response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
            
            if discord_response.status_code in [200, 204]:
                print("Post pushed to your Discord channel feed successfully!")
            else:
                print(f"Discord Webhook rejected payload with status: {discord_response.status_code}")
        else:
            print("Post identifier field missing from the data node object structure.")
    else:
        print("No recent timeline updates returned from the public query engine.")
        # Logs the actual server response so we can instantly diagnose any metadata blocks
        print(f"Server Response: {json.dumps(data)}")

except Exception as e:
    print(f"Error executing raw API web transfer check: {e}")

print("Check complete.")
