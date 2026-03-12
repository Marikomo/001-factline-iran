import os
import requests
import yfinance as yf
from datetime import datetime

# 送信先URL
WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data(event_name=""):
    symbols = {
        "USDJPY": "JPY=X",
        "ILS": "ILS=X",
        "Gold": "GC=F",
        "CrudeOil": "CL=F",
        "S&P500": "^GSPC",
        "SOX": "^SOX",
        "NaturalGas": "NG=F"
    }
    
    results = {"date": datetime.now().strftime("%Y-%m-%d %H:%M")}

    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            price = ticker.fast_info['last_price']
            results[name] = round(price, 2)
        except Exception as e:
            print(f"{name} の取得に失敗: {e}")
            results[name] = ""

    # ↓ ここから下の行の「左側の空白」を上の results = ... と完全に揃えます
    payload = {
        "sheetName": "MarketData",
        "date": results["date"],
        "usdjpy": results["USDJPY"],
        "ils": results["ILS"],
        "gold": results["Gold"],
        "crudeoil": results["CrudeOil"],
        "sp500": results["S&P500"],
        "sox": results["SOX"],
        "gas": results["NaturalGas"],
        "event": event_name
    }

    try:
        res = requests.post(WEBAPP_URL, json=payload)
        print(f"送信データ: {payload}")  # これで中身をログに出します
        print(f"市場データ送信成功: {res.status_code}")
    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    get_market_data()
