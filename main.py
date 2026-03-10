import os
import requests
import google.generativeai as genai
import feedparser
import json
import re

# 1. 準備
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. 旧来の安定した設定方法
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def analyze_and_send():
    # Googleニュース（安定）
    feed = feedparser.parse("https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en")
    
    if not feed.entries:
        print("ニュースが取得できませんでした")
        return

    for entry in feed.entries[:3]:
        prompt = f"""
        Analyze the following news and output in Japanese JSON format.
        News: {entry.title}
        
        Output format (STRICT):
        {{
            "title_en": "{entry.title}",
            "summary_jp": "1.事象 2.背景 3.影響 を各20文字以内の3行で",
            "trust_level": "🔵(確定)/🟡(未確認)/🔴(疑い)",
            "impact": "Economic impact prediction in 1 line",
            "link": "{entry.link}"
        }}
        """
        
        try:
            # 旧来の安定した生成メソッド
            response = model.generate_content(prompt)
            
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                res = requests.post(WEBAPP_URL, json=data)
                print(f"送信結果: {res.status_code}") 
            else:
                print("JSONが見つかりませんでした")
                
        except Exception as e:
            print(f"エラー発生: {e}")

if __name__ == "__main__":
    analyze_and_send()
