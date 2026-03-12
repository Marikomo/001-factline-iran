import os
import requests
import yfinance as yf
import time
from datetime import datetime

WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data(event_name="過去データ一括取得"):
    # 取得したい銘柄
    symbols = {
        "USDJPY": "JPY=X",
        "ILS": "ILS=X",
        "Gold": "GC=F",
        "CrudeOil": "CL=F",
        "S&P500": "^GSPC",
        "SOX": "^SOX",
        "NaturalGas": "NG=F"
    }

    print("2025-06-24からのデータをダウンロード中...")
    
    # 全銘柄の過去データを一括取得
    all_data = {}
    for name, sym in symbols.items():
        # 2025-06-24から今日までの日足データを取得
        df = yf.download(sym, start="2025-06-24")
        all_data[name] = df['Close']
        time.sleep(1) # API負荷軽減

    # 最初に見つかった銘柄の日付リストを基準にする
    first_sym = list(symbols.keys())[0]
    dates = all_data[first_sym].index

    print(f"{len(dates)}日分のデータを送信開始します...")

    for d in dates:
        date_str = d.strftime("%Y-%m-%d")
        
        # 各銘柄のその日の価格を取り出す
        payload = {
            "sheetName": "MarketData",
            "date": date_str,
            "usdjpy": round(float(all_data["USDJPY"].get(d, 0)), 2),
            "ils": round(float(all_data["ILS"].get(d, 0)), 4), # 為替は小数第4位まで
            "gold": round(float(all_data["Gold"].get(d, 0)), 2),
            "crudeoil": round(float(all_data["CrudeOil"].get(d, 0)), 2),
            "sp500": round(float(all_data["S&P500"].get(d, 0)), 2),
            "sox": round(float(all_data["SOX"].get(d, 0)), 2),
            "gas": round(float(all_data["NaturalGas"].get(d, 0)), 2),
            "event": "過去データ一括インポート"
        }

        try:
            res = requests.post(WEBAPP_URL, json=payload)
            print(f"送信: {date_str} -> {res.status_code}")
            time.sleep(0.5) # GASへの連続負荷を避ける
        except Exception as e:
            print(f"エラー ({date_str}): {e}")

if __name__ == "__main__":
    get_market_data()
