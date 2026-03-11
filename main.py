import os
import requests
import feedparser

# SecretsからURLだけ取得
WEBAPP_URL = os.getenv("WEBAPP_URL")

def simple_send():
    # Googleニュース（US版）から取得
    feed = feedparser.parse("https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en")
    
    if not feed.entries:
        print("ニュースが見つかりませんでした")
        return

    # 最新の3件を送信
    for entry in feed.entries[:3]:
        data = {
            "title_en": entry.title,
            "summary_jp": "（AI制限中のため、原文タイトルを参照してください）",
            "trust_level": "🌐",
            "impact": "News fetched successfully",
            "link": entry.link
        }
        try:
            res = requests.post(WEBAPP_URL, json=data)
            print(f"送信成功: {res.status_code}")
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    simple_send()
