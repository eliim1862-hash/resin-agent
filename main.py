import os
import requests
from datetime import datetime, timezone
import anthropic

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]

SYSTEM_PROMPT = """
You are a senior R&D director and technology scout specializing in:
Pressure Sensitive Adhesives (PSA), Acrylic Emulsions, Vinyl Acrylic Resins,
Styrene Acrylic Resins, Water-Based Adhesives, Hot Melt Adhesives,
Reactive Adhesives, Coatings, Sealants, Polymer Emulsions, Sustainable Adhesives.

Write the full report IN PERSIAN (Farsi). Use Markdown with emojis.
Report length: 2500-4000 words.

REPORT STRUCTURE:

🧪 گزارش هوشمند رزین و چسب | {date}

📌 خلاصه اجرایی
(5-8 مهم‌ترین رویداد)

🆕 محصولات جدید
(عنوان، شرکت، ۱۵-۲۰ خط خلاصه، اهمیت فنی، اهمیت تجاری، منبع URL)

📋 پتنت‌های جدید
(عنوان، متقاضی، تاریخ، ۱۵-۲۰ خط خلاصه، کاربرد صنعتی، منبع URL)

🔬 مقالات علمی
(عنوان، نویسندگان، مجله، ۱۵-۲۰ خط خلاصه، یافته‌های کلیدی، منبع URL)

📰 اخبار بازار و صنعت
(عنوان، سازمان، ۱۵-۲۰ خط خلاصه، تأثیر بر صنعت، منبع URL)

💡 فرصت‌های نوآوری
(با رتبه‌بندی: پتانسیل بالا / متوسط / پایین)

🏆 ۳ ایده محصول ارزشمند هفته
(مفهوم، پتانسیل بازار، امکان‌پذیری فنی، اقدام پیشنهادی)

─────────────────
🤖 Resin & Adhesive Intelligence Agent
"""

USER_PROMPT = """
Search the web for the last 24 hours only. Use these queries:

1. "pressure sensitive adhesive" new product 2025
2. acrylic emulsion resin patent 2025 site:patents.google.com OR site:wipo.int
3. styrene acrylic vinyl acrylic resin news today site:icis.com OR site:specialchem.com
4. Henkel OR Arkema OR Bostik OR Synthomer adhesive announcement 2025
5. BASF OR Dow OR Ashland acrylic resin new product 2025
6. sustainable bio-based adhesive resin 2025 site:mdpi.com OR site:acs.org
7. adhesive resin acquisition merger partnership 2025
8. رزین چسب اکریلیک ایران خاورمیانه
9. PSA crosslinker monomer emulsifier innovation 2025
10. "hot melt adhesive" OR "reactive adhesive" innovation 2025

Today: """ + datetime.now(timezone.utc).strftime("%Y-%m-%d") + """

If fewer than 5 news items found in 24h, expand to 72 hours and note it.
Write the complete report in Persian as instructed.
"""

def generate_report() -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": USER_PROMPT}]
    )
    full_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            full_text += block.text
    return full_text or "⚠️ گزارش تولید نشد."

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for part in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        payload = {"chat_id": CHAT_ID, "text": part, "parse_mode": "Markdown", "disable_web_page_preview": True}
        r = requests.post(url, json=payload, timeout=30)
        if not r.json().get("ok"):
            payload.pop("parse_mode")
            requests.post(url, json=payload, timeout=30)

def main():
    print(f"🧪 Agent started — {datetime.now()}")
    report = generate_report()
    send_telegram(report)
    print("✅ Done!")

if __name__ == "__main__":
    main()
