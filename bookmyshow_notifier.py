import cloudscraper
import time
import json
import requests

# === Configuration ===
TARGET_DATE = "20250912"  # The date you're watching for (YYYYMMDD format)

# Telegram Bot Config (Replace with your actual values)
TELEGRAM_BOT_TOKEN = "your_dummy_bot_token" #eg: 123456789:ABCdefGhIjkLmNoPQRstUvwxYZ1234567890
TELEGRAM_CHAT_ID = "your_dummy_chat_id" #eg: 123456789

# === Telegram Notifier ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print("❌ Failed to send Telegram message:", response.text)
    except Exception as e:
        print("⚠️ Telegram error:", e)

# === BookMyShow Scraper ===
scraper = cloudscraper.create_scraper(
    interpreter='js2py',  # Required to bypass Cloudflare
)

def fetch():
    timestamp = str(int(time.time() * 1000))
    url = (
        "https://in.bookmyshow.com/ibvcom/getJSData.bms"
        "?cmd=GETSHOWDATESBYEVENT"
        "&eid=ET00436673"     # Event ID (change this as per your movie)
        "&srid=HYD"           # Sub-region ID (e.g., HYD = Hyderabad)
        "&cid=ASMB"           # Cinema ID (e.g., ASMB = AMB Cinemas)
        "&pid="               # Optional
        "&ety=MT"             # Event type: MT = Movie
        f"&s={timestamp}"
    )

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Requesting: {url}")
    try:
        response = scraper.get(url)
    except Exception as e:
        print("❌ Request failed:", e)
        send_telegram_message("❌ BookMyShow request failed.")
        return

    if response.status_code != 200:
        print("❌ Failed to fetch data.")
        send_telegram_message("❌ Failed to fetch BookMyShow show dates.")
        return

    text = response.text.strip()

    if text.startswith("arrShowDates="):
        json_data = text[len("arrShowDates="):].rstrip(';')
        try:
            show_dates = json.loads(json_data)
        except json.JSONDecodeError:
            print("❌ JSON decode error")
            send_telegram_message("⚠️ Couldn't parse BookMyShow response.")
            return

        found = False
        date_list = []

        for entry in show_dates:
            # Format: [index, "Day", "Display Date", "20250913", "Display Date"]
            date_str = f"{entry[4]} ({entry[3]})"
            date_list.append(date_str)
            if entry[3] == TARGET_DATE:
                found = True

        if found:
            msg = f"✅ 🎉 *Target date {TARGET_DATE} is available!*\n\n📅 All dates:\n" + "\n".join(date_list)
            print(msg)
            send_telegram_message(msg)
        else:
            msg = f"❌ Target date {TARGET_DATE} not found.\n\n📅 Available:\n" + "\n".join(date_list)
            print(msg)
            send_telegram_message(msg)
    else:
        print("⚠️ Unexpected response format or blocked request:")
        print(text[:300])
        send_telegram_message("⚠️ BookMyShow response format unexpected or request blocked.")

# === Loop to run every 15 minutes ===
if __name__ == "__main__":
    while True:
        fetch()
        print("🔁 Sleeping for 15 minutes...\n")
        time.sleep(900)  # 900 seconds = 15 minutes
