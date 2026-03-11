import os
import requests
import yfinance as yf
from datetime import datetime

# 送信先URL
WEBAPP_URL = os.getenv("WEBAPP_URL")

# 修正前：def get_market_data():
# 修正後：event_nameを受け取れるようにします
def get_market_data(event_name=""): 
    # ... 中略 ...
    payload = {
        # ... 中略 ...
        "event": event_name # results.getではなく、引数のevent_nameを使う
    }
    
    results = {"date": datetime.now().strftime("%Y-%m-%d %H:%M")}

    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            price = ticker.fast_info['last_price']
            results[name] = round(price, 2)
        except Exception as e:
            print(f"{name} の取得に失敗: {e}")
            results[name] = "N/A"

    # --- ここを修正しました ---
    payload = {
        "sheetName": "MarketData",
        "date": results["date"],
        "usdjpy": results["USDJPY"],
        "gold": results["Gold"],
        "crudeoil": results["CrudeOil"],
        "sp500": results["S&P500"],
        "sox": results["SOX"],
        "gas": results["NaturalGas"],
        "event": "" # ← ここにイベント名が入る器を作りました
    }
    # -----------------------

    try:
        res = requests.post(WEBAPP_URL, json=payload)
        print(f"市場データ送信成功: {res.status_code}")
    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    get_market_data()
