import os
import requests
from datetime import datetime, timezone
import anthropic

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()

SYSTEM_PROMPT = """You are a senior R&D director and technology scout specializing in Pressure Sensitive Adhesives (PSA), Acrylic Emulsions, Vinyl Acrylic Resins, Styrene Acrylic Resins, Water-Based Adhesives, Hot Melt Adhesives, Reactive Adhesives, Coatings, Sealants, Polymer Emulsions, Sustainable Adhesives. Write the full report IN PERSIAN (Farsi). Use Markdown with emojis. Report length: 2500-4000 words. REPORT STRUCTURE: 🧪 گزارش هوشمند رزین و چسب | {date} 📌 خلاصه اجرایی (5-8 مهم‌ترین رویداد) 🆕 محصولات جدید (عنوان، شرکت، 15-20 خط خلاصه، اهمیت فنی، اهمیت تجاری، منبع URL) 📋 پتنت‌های جدید (عنوان، متقاضی، تاریخ، 15-20 خط خلاصه، کاربرد صنعتی، منبع URL) 🔬 مقالات علمی (عنوان، نویسندگان، مجله، 15-20 خط خلاصه، یافته‌های کلیدی، منبع URL) 📰 اخبار بازار و صنعت (عنوان، سازمان، 15-20 خط خلاصه، تاثیر بر صنعت، منبع URL) 💡 فرصت‌های نوآوری (با رتبه‌بندی: پتانسیل بالا / متوسط / پایین) 🏆 3 ایده محصول ارزشمند هفته (مفهوم، پتانسیل بازار، امکان‌پذیری فنی، اقدام پیشنهادی) ─────────────────  🤖 Resin & Adhesive Intelligence Agent"""

def generate_report():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    user_prompt = "Search the web for the last 24 hours only. Queries: 1. pressure sensitive adhesive new product 2025 2. acrylic emulsion resin patent 2025 3. styrene acrylic vinyl acrylic resin news 4. Henkel OR Arkema OR Synthomer adhesive 2025 5. BASF OR Dow acrylic resin new 2025 6. sustainable bio-based adhesive 2025 7. adhesive resin acquisition merger 2025 8. PSA crosslinker monomer innovation 2025. Today: " + today + ". Write the complete report in Persian."
    api_key = os.environ["ANTHROPIC_API_KEY"].strip()
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": user_prompt}]
    )
    full_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            full_text += block.text
    return full_text or "گزارش تولید نشد."

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
    send_telegram(report)
    print("Done!")

if __name__ == "__main__":
    main()
