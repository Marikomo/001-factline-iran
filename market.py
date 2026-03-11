import os
import requests
import yfinance as yf
from datetime import datetime

# 送信先URL（Newsの時と同じものでOK）
WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data():
    # 取得したい銘柄のリスト（Yahoo Financeのシンボル）
    # JPY=X: ドル円, GC=F: 金先物, CL=F: 原油先物, ^GSPC: S&P500, ^SOX: 半導体指数, NG=F: 天然ガス
    symbols = {
        "USDJPY": "JPY=X",
        "Gold": "GC=F",
        "CrudeOil": "CL=F",
        "S&P500": "^GSPC",
        "SOX": "^SOX",
        "NaturalGas": "NG=F"
    }
    
    # 今日の日付
    results = {"date": datetime.now().strftime("%Y-%m-%d %H:%M")}

    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            # 最新の終値を取得
            price = ticker.fast_info['last_price']
            results[name] = round(price, 2)
        except:
            results[name] = "N/A"

    # スプレッドシート（GAS）に送るデータ
    # ※sheetNameを指定することで、MarketDataタブに書き込むようにします
    payload = {
        "sheetName": "MarketData",
        "date": results["date"],
        "usdjpy": results["USDJPY"],
        "gold": results["Gold"],
        "crudeoil": results["CrudeOil"],
        "sp500": results["S&P500"],
        "sox": results["SOX"],
        "gas": results["NaturalGas"]
    }

    try:
        res = requests.post(WEBAPP_URL, json=payload)
        print(f"市場データ送信成功: {res.status_code}")
    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    get_market_data()
