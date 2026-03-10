import os
import requests
import google.generativeai as genai
import feedparser
import json
import re

# 1. 準備
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. AIの設定
genai.configure(api_key=GEMINI_KEY)
# 最もエラーが起きにくい名前に固定します
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_and_send():
    # Googleニュースから取得
    feed = feedparser.parse("https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en")
    
    for entry in feed.entries[:3]:
        prompt = f"""
        Analyze the following news and output in Japanese JSON format.
        News: {entry.title}
        
        Output format (STRICT):
        {{
            "title_en": "{entry.title}",
            "summary_jp": "1.事象 2.背景 3.影響 を各20文字以内の3行で",
            "trust_level": "🔵(確定)/🟡(未確認)/🔴(疑い)",
            "impact": "今後の経済への影響を1行で",
            "link": "{entry.link}"
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            
            if match:
                data = json.loads(match.group())
                # スプレッドシートに送信
                res = requests.post(WEBAPP_URL, json=data)
                print(f"送信結果: {res.status_code}")
            else:
                print("JSONが見つかりませんでした")
                
        except Exception as e:
            print(f"AIエラー: {e}")

if __name__ == "__main__":
    analyze_and_send()
