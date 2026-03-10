import os
import requests
from google import genai
import feedparser
import json
import re

# 1. 準備：Secretsから値を取得
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. AIの設定 (最新の google-genai 形式)
client = genai.Client(api_key=GEMINI_KEY)

def analyze_and_send():
    # ロイターのニュースを取得
    feed = feedparser.parse("https://www.reutersagency.com/feed/?best-sectors=world-news&post_type=best")
    
    if not feed.entries:
        print("ニュースが取得できませんでした")
        return

    for entry in feed.entries[:3]: # 最新3件
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
            # 最新の生成方法に変更
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            # AIの回答から { } の部分だけを抽出
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            
            if match:
                json_str = match.group()
                data = json.loads(json_str)
                
                # スプレッドシート（GAS）に送信
                res = requests.post(WEBAPP_URL, json=data)
                print(f"送信結果: {res.status_code}") 
            else:
                print("JSON形式の回答が得られませんでした")
                
        except Exception as e:
            print(f"エラー発生: {e}")

if __name__ == "__main__":
    analyze_and_send()
