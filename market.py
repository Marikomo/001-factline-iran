# v2 - 過去データ強制インポート用
import os
import requests
import yfinance as yf
import time

WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data(event_name="一括インポート"):
    # これがログに出れば成功
    print("★★★ 2025年からのデータを取得しにいきます ★★★")
    
    symbols = {
        "USDJPY": "JPY=X", "ILS": "ILS=X", "Gold": "GC=F",
        "CrudeOil": "CL=F", "S&P500": "^GSPC", "SOX": "^SOX", "NaturalGas": "NG=F"
    }

    all_data = {}
    for name, sym in symbols.items():
        print(f"{name}を取得中...")
        df = yf.download(sym, start="2025-06-24")
        all_data[name] = df['Close']
        time.sleep(0.5)

    dates = all_data["USDJPY"].index
    print(f"合計 {len(dates)} 日分のデータを送信します。")

    for d in dates:
        date_str = d.strftime("%Y-%m-%d")
        payload = {
            "sheetName": "MarketData",
            "date": date_str,
            "usdjpy": round(float(all_data["USDJPY"].get(d, 0)), 2),
            "ils": round(float(all_data["ILS"].get(d, 0)), 4),
            "gold": round(float(all_data["Gold"].get(d, 0)), 2),
            "crudeoil": round(float(all_data["CrudeOil"].get(d, 0)), 2),
            "sp500": round(float(all_data["S&P500"].get(d, 0)), 2),
            "sox": round(float(all_data["SOX"].get(d, 0)), 2),
            "gas": round(float(all_data["NaturalGas"].get(d, 0)), 2),
            "event": "履歴データ(GitHub経由)"
        }
        res = requests.post(WEBAPP_URL, json=payload)
        print(f"送信完了: {date_str} ({res.status_code})")
        time.sleep(0.3)

if __name__ == "__main__":
    get_market_data()
