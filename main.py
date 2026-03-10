import os
import requests
import google.generativeai as genai
import feedparser
import json
import re
import time

# 1. 準備
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 2. AIの設定
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def analyze_and_send():
    feed = feedparser.parse("https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en")
    
    # 制限にかかりにくくするため、まずは「最新の1件」だけでテストします
    for entry in feed.entries[:1]: 
        prompt = f"Analyze and output in Japanese JSON: {entry.title}" # プロンプトを短くして負荷を減らす
        
        try:
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            
            if match:
                data = json.loads(match.group())
                res = requests.post(WEBAPP_URL, json=data)
                print(f"成功！送信結果: {res.status_code}")
            else:
                # JSONじゃなくても、要約文があればそのまま送る工夫
                data = {"title_en": entry.title, "summary_jp": response.text[:50], "link": entry.link}
                requests.post(WEBAPP_URL, json=data)
                print("要約文として送信しました")
                
        except Exception as e:
            print(f"AIエラー: {e}")
        
        time.sleep(2) # 2秒待機（これ大事！）

if __name__ == "__main__":
    analyze_and_send()
