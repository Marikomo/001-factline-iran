import os
import requests
import google.generativeai as genai
import feedparser
import json

# 1. 準備：Secretsから合鍵を取り出す
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. AIの設定
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_news():
    # ロイターの世界ニュースRSSを使用
    feed_url = "https://www.reutersagency.com/feed/?best-sectors=world-news&post_type=best"
    feed = feedparser.parse(feed_url)
    return feed.entries[:3]  # 最新3件をチェック

def analyze_and_send():
    articles = get_news()
    for entry in articles:
        prompt = f"""
        以下の英語ニュースを分析し、ビジネスマン向けに日本語のJSON形式のみで出力してください。
        ニュース: {entry.title} - {entry.summary}
        
        回答形式：
        {{
            "title_en": "元の英語見出し",
            "summary_jp": "1.事象 2.背景 3.影響 を各20文字以内の3行で",
            "trust_level": "🔵(確定)/🟡(未確認)/🔴(疑い)から1つ",
            "impact": "経済への影響予測を1行で",
            "link": "{entry.link}"
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            # AIの回答からJSONを抽出
            text = response.text.strip().replace('```json', '').replace('```', '')
            data = json.loads(text)
            
            # Googleスプレッドシートに送信
            requests.post(WEBAPP_URL, json=data)
            print(f"送信成功: {data['title_en']}")
        except Exception as e:
            print(f"エラー発生: {e}")

if __name__ == "__main__":
    analyze_and_send()
