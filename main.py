import os
import requests
from datetime import datetime, timezone

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"].strip()

SYSTEM_PROMPT = "You are a senior R&D director specializing in Pressure Sensitive Adhesives, Acrylic Emulsions, Vinyl Acrylic Resins, Styrene Acrylic Resins, Coatings and Sealants. Write a detailed intelligence report IN PERSIAN (Farsi) with emojis and Markdown formatting covering: new products, patents, research papers, market news, innovation opportunities, and top 3 product ideas."

def generate_report():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    user_prompt = "Today is " + today + ". Write a detailed R&D intelligence report in Persian about the latest news in pressure sensitive adhesives, acrylic emulsions, vinyl acrylic, styrene acrylic and resin technology. Include sections for new products, patents, research papers, market news, innovation opportunities and top 3 product ideas worth developing."
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": "Bearer " + OPENROUTER_API_KEY, "Content-Type": "application/json"},
        json={"model": "meta-llama/llama-3.3-70b-instruct:free", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}], "max_tokens": 4000},
        timeout=120
    )
    print("Status: " + str(response.status_code))
    data = response.json()
    print("Response preview: " + str(data)[:300])
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    elif "error" in data:
        return "خطا: " + str(data["error"])
    else:
        return "پاسخ نامعلوم: " + str(data)[:200]

def send_telegram(text):
    url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    for part in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        payload = {"chat_id": CHAT_ID, "text": part, "parse_mode": "Markdown", "disable_web_page_preview": True}
        r = requests.post(url, json=payload, timeout=30)
        if not r.json().get("ok"):
            payload.pop("parse_mode")
            requests.post(url, json=payload, timeout=30)

def main():
    print("Agent started — " + str(datetime.now()))
    report = generate_report()
    print("Report length: " + str(len(report)))
    send_telegram(report)
    print("Done!")

if __name__ == "__main__":
    main()
