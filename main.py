import os
import requests
from datetime import datetime, timezone

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"].strip()

SYSTEM_PROMPT = """You are a senior R&D director and technology scout specializing in Pressure Sensitive Adhesives (PSA), Acrylic Emulsions, Vinyl Acrylic Resins, Styrene Acrylic Resins, Water-Based Adhesives, Hot Melt Adhesives, Reactive Adhesives, Coatings, Sealants, Polymer Emulsions, Sustainable Adhesives. Write the full report IN PERSIAN (Farsi). Use Markdown with emojis. Report length: 2500-4000 words. REPORT STRUCTURE: 🧪 گزارش هوشمند رزین و چسب | {date} 📌 خلاصه اجرایی (5-8 مهم‌ترین رویداد) 🆕 محصولات جدید (عنوان، شرکت، 15-20 خط خلاصه، اهمیت فنی، اهمیت تجاری، منبع URL) 📋 پتنت‌های جدید (عنوان، متقاضی، تاریخ، 15-20 خط خلاصه، کاربرد صنعتی، منبع URL) 🔬 مقالات علمی (عنوان، نویسندگان، مجله، 15-20 خط خلاصه، یافته‌های کلیدی، منبع URL) 📰 اخبار بازار و صنعت (عنوان، سازمان، 15-20 خط خلاصه، تاثیر بر صنعت، منبع URL) 💡 فرصت‌های نوآوری (با رتبه‌بندی: پتانسیل بالا / متوسط / پایین) 🏆 3 ایده محصول ارزشمند هفته (مفهوم، پتانسیل بازار، امکان‌پذیری فنی، اقدام پیشنهادی) ─────────────────  🤖 Resin & Adhesive Intelligence Agent"""

def generate_report():
    def generate_report():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    user_prompt = f"Today is {today}. Write a detailed R&D intelligence report in Persian about the latest news in pressure sensitive adhesives, acrylic emulsions, and resin technology. Include sections for new products, patents, research papers, and market news. Add innovation opportunities and top 3 product ideas."

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 4000,
        },
        timeout=120
    )

    print(f"Status code: {response.status_code}")
    data = response.json()
    print(f"Response: {str(data)[:500]}")
    
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    elif "error" in data:
        return f"خطای API: {data['error']}"
    else:
        return f"پاسخ نامعلوم: {str(data)[:200]}"
   

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for part in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        payload = {"chat_id": CHAT_ID, "text": part, "parse_mode": "Markdown", "disable_web_page_preview": True}
        r = requests.post(url, json=payload, timeout=30)
        if not r.json().get("ok"):
            payload.pop("parse_mode")
            requests.post(url, json=payload, timeout=30)

def main():
    print(f"Agent started — {datetime.now()}")
    report = generate_report()
    print(f"Report generated — {len(report)} chars")
    send_telegram(report)
    print("Done!")

if __name__ == "__main__":
    main()
