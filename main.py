import os
import requests
import feedparser
from datetime import datetime
import market  # market.pyを呼び出すために追加

# 環境変数の取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_gemini_summary(text):
    # AIへの指示（プロンプト）
    # ニュースの要約と一緒に、チャート用の「イベント名」も作らせます
    prompt = f"""
    以下のニュース群から、地政学・経済的に最も重要なニュースを要約してください。
    また、そのニュースを一言（10文字以内）で表すチャート用の「イベント名」を1つだけ作成してください。
    
    出力形式：
    EVENT: [イベント名]
    SUMMARY:
    [要約内容を箇条書きで]

    ニュース：
    {text}
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        res = requests.post(url, json=payload)
        output = res.json()['candidates'][0]['content']['parts'][0]['text']
        return output
    except:
        return "EVENT: なし\nSUMMARY: 要約に失敗しました。"

def main():
    # RSSフィードからニュース取得（例としてReuters）
    d = feedparser.parse("https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best")
    news_text = "\n".join([entry.title for entry in d.entries[:10]])
    
    full_output = get_gemini_summary(news_text)
    
    # AIの回答から「EVENT:」と「SUMMARY:」を切り分ける
    event_name = "なし"
    summary_jp = full_output
    if "EVENT:" in full_output:
        parts = full_output.split("SUMMARY:")
        event_name = parts[0].replace("EVENT:", "").strip()
        summary_jp = parts[1].strip() if len(parts) > 1 else full_output

    # 1. ニュースをスプレッドシートに送信
    news_payload = {
        "title_en": "Daily Geopolitics News",
        "summary_jp": summary_jp,
        "trust_level": "High",
        "impact": "Medium",
        "link": d.entries[0].link if d.entries else ""
    }
    requests.post(WEBAPP_URL, json=news_payload)

    # 2. 市場データを取得して、AIが決めた「event_name」を載せて送信
    # ※market.pyの関数を呼び出します
    print(f"抽出されたイベント: {event_name}")
    market.get_market_data(event_name) # ここでイベント名を渡す

if __name__ == "__main__":
    main()
