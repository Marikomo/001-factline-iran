import os
import requests
import feedparser

# SecretsからURLだけ取得（AIキーは使いません）
WEBAPP_URL = os.getenv("WEBAPP_URL")

def simple_send():
    # Googleニュースから取得
    feed = feedparser.parse("https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en")
    
    for entry in feed.entries[:3]:
        # AIを通さず、そのままデータを整形
        data = {
            "title_en": entry.title,
            "summary_jp": "（AI要約は現在停止中。通信テストです）",
            "trust_level": "⚪️",
            "impact": "Testing...",
            "link": entry.link
        }
        # スプレッドシートに送信
        try:
            res = requests.post(WEBAPP_URL, json=data)
            print(f"送信結果: {res.status_code}")
        except Exception as e:
            print(f"送信エラー: {e}")

if __name__ == "__main__":
    simple_send()
