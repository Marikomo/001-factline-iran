import os
import requests
from google import genai
import feedparser
import json
import re

# 1. 準備
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. AIの設定
client = genai.Client(api_key=GEMINI_KEY)

def analyze_and_send():
    # Googleニュースから取得（一番安定しています）
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
            # モデル名の指定方法を最もシンプルな形に変更
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                json_str = match.group()
                data = json.loads(json_str)
                
                # スプレッドシートに送信
                res = requests.post(WEBAPP_URL, json=data)
                print(f"送信結果: {res.status_code}") 
            else:
                print("JSON形式の回答が得られませんでした")
                
        except Exception as e:
            # もし「gemini-1.5-flash」がダメなら、自動的に予備の「gemini-2.0-flash」を試す
            try:
                response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                # (以下、同様の処理)
                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if match:
                    data = json.loads(match.group())
                    res = requests.post(WEBAPP_URL, json=data)
                    print(f"予備モデルで成功: {res.status_code}")
            except:
                print(f"エラー発生: {e}")

if __name__ == "__main__":
    analyze_and_send()
