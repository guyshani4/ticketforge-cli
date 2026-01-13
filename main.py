import requests
import json
import sys
import os
import time

# הגדרת צבעים לטרמינל (Innovation: UI improvements)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

BASE_URL = "https://integrations-assignment-ticketforge.vercel.app"
CONFIG_FILE = 'config.json'

def get_headers():
    """
    Load the saved Basic Auth token from the local configuration file and build
    the HTTP headers used for all TicketForge API requests.

    Exits the program with an error message if the configuration file does not exist.
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"{RED}❌ Error: Configuration not found. Run 'python3 main.py setup <token>'{RESET}")
        sys.exit(1)
    with open(CONFIG_FILE, 'r') as f:
        token = json.load(f).get("token")
    
    return {
        "Authorization": f"Basic {token}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"{BASE_URL}/mine",
        "X-Requested-With": "XMLHttpRequest"
    }


def handle_response(response):
    """
    Perform generic handling of HTTP responses, including rate-limiting and
    common error codes.

    - If status is 429, informs the user and sleeps briefly before allowing a retry.
    - For 404 and 401, prints a human-readable explanation and returns None.
    - For all other statuses, returns the original response object unchanged.
    """
    if response.status_code == 429:
        print(f"{YELLOW}⚠️ Rate limit encountered. Retrying in 2 seconds...{RESET}")
        time.sleep(2)
        return None
    if response.status_code == 404:
        print(f"{RED}❌ Error 404: Resource not found. The server might be blocking non-browser requests.{RESET}")
        return None
    if response.status_code == 401:
        print(f"{RED}❌ Error 401: Unauthorized. Please check your token in 'setup'.{RESET}")
        return None
    return response

def list_tickets():
    """
    Fetch and display a table of tickets for the current user.

    Tries the `/api/tickets` endpoint first and falls back to `/api/mine`
    if the first call fails, printing helpful status messages along the way.
    """
    url = f"{BASE_URL}/api/tickets" 
    print(f"{CYAN}🔍 Fetching tickets from: {url}...{RESET}")
    
    try:
        response = requests.get(url, headers=get_headers())
        res = handle_response(response)
        
        if res and res.status_code == 200:
            tickets = res.json()
            print(f"{GREEN}✅ Successfully retrieved {len(tickets)} tickets:{RESET}\n")
            print(f"{'ID':<5} | {'Title':<20} | {'Status':<10}")
            print("-" * 40)
            for t in tickets:
                print(f"{t.get('id'):<5} | {t.get('title')[:20]:<20} | {t.get('status'):<10}")
        else:
            print(f"{YELLOW}🔄 Attempting alternative path (/api/mine)...{RESET}")
            response = requests.get(f"{BASE_URL}/api/mine", headers=get_headers())
            if response.status_code == 200:
                print(f"{GREEN}✅ Found tickets on alternative path!{RESET}")
                print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"{RED}❌ Connection error: {e}{RESET}")

def save_config(token):
    """
    Persist the provided Base64 token into the local JSON configuration file.

    Automatically strips a leading 'Basic ' prefix if present and writes the
    normalized token to `config.json`, then notifies the user.
    """
    token = token.replace("Basic ", "").strip()
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"token": token}, f)
    print(f"{GREEN}✅ Setup complete! Configuration saved to {CONFIG_FILE}.{RESET}")

def main():
    """
    Command-line entry point for the TicketForge CLI.

    Parses `sys.argv` and routes to the appropriate subcommand:
    - `setup <token>`: saves the Basic Auth token to local config
    - `list`: lists tickets using the configured token
    Other commands are acknowledged but currently unimplemented.
    """
    print(f"{CYAN}--- TicketForge CLI Manager ---{RESET}")
    if len(sys.argv) < 2:
        print("Usage: python3 main.py [setup|list|create|update]")
        return

    cmd = sys.argv[1].lower()
    if cmd == "setup":
        token = sys.argv[2] if len(sys.argv) > 2 else input("Enter your Base64 token: ")
        save_config(token)
    elif cmd == "list":
        list_tickets()
    else:
        print(f"{YELLOW}Command '{cmd}' is recognized but requires further API reverse engineering to implement successfully.{RESET}")

if __name__ == "__main__":
    main()