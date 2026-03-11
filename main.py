import os
import requests
from google import genai
import feedparser
import json
import re

# 1. 準備
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. アメリカ拠点（v1）を明示的に指定して接続
client = genai.Client(
    api_key=GEMINI_KEY,
    http_options={'api_version': 'v1'}
)

def analyze_and_send():
    feed = feedparser.parse("https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en")
    
    for entry in feed.entries[:1]: 
        prompt = f"Analyze this news and output in Japanese JSON format: {entry.title}"
        
        try:
            # モデル名を指定して実行
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                res = requests.post(WEBAPP_URL, json=data)
                print(f"成功！送信結果: {res.status_code}")
            else:
                summary = response.text[:100].replace('\n', ' ')
                data = {"title_en": entry.title, "summary_jp": summary, "link": entry.link}
                requests.post(WEBAPP_URL, json=data)
                print("成功（テキスト送信）")
                
        except Exception as e:
            print(f"AIエラー発生: {e}")

if __name__ == "__main__":
    analyze_and_send()
