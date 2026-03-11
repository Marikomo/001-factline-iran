import os
import requests
from google import genai
import feedparser
import json
import re

# 1. 準備
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. 最新の GenAI クライアント作成
client = genai.Client(api_key=GEMINI_KEY)

def analyze_and_send():
    # Googleニュース（US版）から取得
    feed = feedparser.parse("https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en")
    
    for entry in feed.entries[:1]: 
        prompt = f"Analyze this news and output in Japanese JSON format: {entry.title}"
        
        try:
            # 最新の generate_content メソッド
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            # AIの回答から JSON 部分を抽出
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                res = requests.post(WEBAPP_URL, json=data)
                print(f"成功！送信結果: {res.status_code}")
            else:
                # JSONが見つからない場合はテキストとして送信
                summary = response.text[:100].replace('\n', ' ')
                data = {"title_en": entry.title, "summary_jp": summary, "link": entry.link}
                requests.post(WEBAPP_URL, json=data)
                print("要約テキストを送信しました")
                
        except Exception as e:
            print(f"AIエラー発生: {e}")

if __name__ == "__main__":
    analyze_and_send()
