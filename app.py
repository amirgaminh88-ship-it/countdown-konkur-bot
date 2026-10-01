import os
import time
from datetime import datetime, timezone, timedelta

import requests

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"

TARGET = datetime(2027, 7, 2, 0, 0, 0, tzinfo=timezone.utc)


def countdown():
    now = datetime.now(timezone.utc)
    diff = TARGET - now

    if diff.total_seconds() <= 0:
        return "🎓 کنکور ۱۴۰۶ فرا رسیده!"

    total = int(diff.total_seconds())

    days = total // 86400
    hours = (total % 86400) // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60

    return (
        "🎓 شمارش معکوس کنکور ۱۴۰۶\n\n"
        "📅 ۱۱ تیر ۱۴۰۶\n\n"
        f"⏳ {days} روز\n"
        f"⏰ {hours} ساعت\n"
        f"⏱ {minutes} دقیقه و {seconds} ثانیه"
    )


def send_message(chat_id):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": countdown()
        },
        timeout=20
    )


def main():
    offset = None

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={"timeout": 30, "offset": offset},
                timeout=40
            ).json()

            for update in response.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")
                if not message:
                    continue

                text = message.get("text", "")
                chat_id = message["chat"]["id"]

                if text in ["/start", "/time", "/konkur"]:
                    send_message(chat_id)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
