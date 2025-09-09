# BMS-AMB-cinema-Telegram-Bot
This script monitors the availability of a specific date (e.g., for a movie or event) on BookMyShow  — particularly for AMB Cinemas, Hyderabad — and sends a Telegram alert when that date becomes available.

---

## 📦 Features

- ✅ Scrapes BookMyShow's internal API.
- 🔁 Runs every 15 minutes.
- 📅 Checks for a specific target date.
- 📲 Sends Telegram messages with results.
- 🛠️ Lightweight, customizable, and extendable.

---

## 🚀 Quick Start

### 1. Clone or Download the Script

```bash
https://github.com/Harshil-94/BMS-AMB-cinema-Telegram-Bot.git
cd BMS-AMB-cinema-Telegram-Bot
```

### 2. Install Dependencies
```bash
pip install cloudscraper requests
```

### 3. Configure the Script

Edit the following in bookmyshow_notifier.py:
```bash
TARGET_DATE = "20250913"  # Target date in YYYYMMDD format

TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
```
- ✅ Use @BotFather on Telegram to create a bot.
- 🔍 Use @getidsbot to get your Telegram chat ID.

### 🖥️ Usage

Run the script:
```bash
python bookmyshow_notifier.py
```

The script will:
- Continuously check every 15 minutes.
- Send a Telegram notification if the target date is available.

### 📡 API Breakdown – Reverse Engineering BookMyShow

The script uses BookMyShow's endpoint:

```bash
https://in.bookmyshow.com/ibvcom/getJSData.bms
```

Query Parameters:
| Param  | Description                               |
| ------ | ----------------------------------------- |
| `cmd`  | `GETSHOWDATESBYEVENT` – fetch show dates  |
| `eid`  | Event ID for the movie                    |
| `srid` | Sub-region ID (HYD = Hyderabad)           |
| `cid`  | Cinema ID (ASMB = AMB Cinemas)            |
| `pid`  | Empty (reserved)                          |
| `ety`  | Event type: MT for Movie                  |
| `s`    | Current timestamp (ms) to prevent caching |


### How to Get Event ID:

- Open BookMyShow=>"https://ambcinemas.in/ticket2.html"
- Select desired movie at AMB Cinemas.
- Open browser Developer Tools → Network tab
- Look for a request to getJSData.bms with parameters.
- Extract eid, cid, srid.

📲 Telegram Message Example

```bash
✅ 🎉 Target date 20250913 is available!

📅 All dates:
13 Sep (20250913)
14 Sep (20250914)
```

⚠️ Notes & Usage Warnings

⚠️ BookMyShow uses Cloudflare protection and private APIs.

This script accesses an undocumented internal endpoint intended for frontend use.
Abuse may lead to:
- ❌ IP rate-limiting or banning
- ❌ Cloudflare CAPTCHA blocks
- ❌ API structure changes without notice

✅ Use responsibly:
- ⏱️ Limit frequency (every 15 mins is ideal)
- ⚠️ Don't run too many instances
- 🎯 Avoid scraping multiple cinemas or events aggressively

📝 License
- This project is licensed under the MIT License.
- Use freely at your own risk.

❤️ Support
- This project is intended for personal and educational use only.
- Contributions, issues, and suggestions are welcome.


