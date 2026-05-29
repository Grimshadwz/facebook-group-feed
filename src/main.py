import os
import base64
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

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

# FIXED: Explicitly using mbasic and adding the missing forward slash
url = f"https://facebook.com/{FACEBOOK_ID}"
print(f"Requesting public page timeline for ID: {FACEBOOK_ID}...")

try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    found_url = None
    
    # Scan every single link element on the page using a formal HTML parser engine
    for link in soup.find_all('a', href=True):
        href = link['href']
        
        # Identify standard timeline update links
        if "/story.php" in href or "/permalink.php" in href or "/posts/" in href:
            found_url = href.split("?")[0] if "/posts/" in href else href
            break
        # Identify image uploads / standalone photo link layouts
        elif "/photo.php" in href or "/photos/" in href:
            found_url = href
            break

    if found_url:
        clean_path = found_url.replace("&amp;", "&")
        # Build the final desktop-friendly Facebook post URL address
        full_post_url = f"https://www.facebook.com{clean_path}" if clean_path.startswith("/") else clean_path
        print(f"Match found! Direct Link: {full_post_url}")
        
        payload = {"content": f"Check out my latest Facebook post: {full_post_url}"}
        discord_response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        
        # FIXED: Corrected syntax structure for the status check loop
        if discord_response.status_code in [200, 204]:
            print("Post found and sent to Discord successfully!")
        else:
            print(f"Discord Webhook rejected request with status: {discord_response.status_code}")
    else:
        print("No new recent timeline posts identified in the current layout view.")
        print("--- PAGE DATA SNIPPET FOR DEBUGGING ---")
        print(response.text[:1000].replace('\n', ' '))

except Exception as e:
    print(f"Error executing web transfer check: {e}")

print("Check complete.")
