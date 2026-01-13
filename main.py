import requests
import json
import sys
import os

BASE_URL = "https://integrations-assignment-ticketforge.vercel.app"
CONFIG_FILE = 'config.json'

def get_headers():
    if not os.path.exists(CONFIG_FILE):
        print("❌ Error: Run 'setup' first.")
        sys.exit(1)
    with open(CONFIG_FILE, 'r') as f:
        token = json.load(f).get("token")
    
    # הוספת Headers שיגרמו לסקריפט להיראות כמו דפדפן
    return {
        "Authorization": f"Basic {token}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://integrations-assignment-ticketforge.vercel.app/mine",
        "X-Requested-With": "XMLHttpRequest"
    }

def list_tickets():
    # הנתיב המדויק מה-Network tab בסטטוס 200
    url = f"{BASE_URL}/api/tickets" 
    print(f"Connecting to: {url}...")
    
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            print("✅ Success! Found the API.")
            print(json.dumps(response.json(), indent=2))
        else:
            # אם זה עדיין נכשל, ננסה את הנתיב החלופי
            print(f"Attempting alternative path...")
            response = requests.get(f"{BASE_URL}/api/mine", headers=get_headers())
            if response.status_code == 200:
                 print("✅ Success on alternative path!")
                 print(json.dumps(response.json(), indent=2))
            else:
                print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def save_config(token):
    token = token.replace("Basic ", "").strip()
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"token": token}, f)
    print("✅ Setup complete!")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "setup":
        token = sys.argv[2] if len(sys.argv) > 2 else input("Token: ")
        save_config(token)
    elif cmd == "list":
        list_tickets()