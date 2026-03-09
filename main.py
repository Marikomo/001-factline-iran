import os
import requests
import google.generativeai as genai
import feedparser
import json
import re

# 1. 準備：Secretsから合鍵を取り出す
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. AIの設定
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_and_send():
    # ロイターの最新ニュースを取得
    feed = feedparser.parse("https://www.reutersagency.com/feed/?best-sectors=world-news&post_type=best")
    
    for entry in feed.entries[:3]: # 最新3件を処理
        # AIへの指示：必ずJSON形式で出すように厳命
        prompt = f"""
        Analyze the following news and output in Japanese JSON format.
        News: {entry.title}
        
        Output format (STRICT):
        {{
            "title_en": "Original English Title",
            "summary_jp": "1.事象 2.背景 3.影響 を各20文字以内の3行で",
            "trust_level": "🔵(確定)/🟡(未確認)/🔴(疑い)",
            "impact": "Economic impact prediction in 1 line",
            "link": "{entry.link}"
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            # AIの回答から { } の部分だけを抽出する（正規表現）
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            
            if match:
                json_str = match.group()
                data = json.loads(json_str)
                
                # Googleスプレッドシート（GAS）に送信
                res = requests.post(WEBAPP_URL, json=data)
                print(f"送信結果: {res.status_code}") # 200なら成功
            else:
                print("JSONが見つかりませんでした")
                
        except Exception as e:
            print(f"エラー発生: {e}")

if __name__ == "__main__":
    analyze_and_send()
