import os
import requests
import yfinance as yf
from datetime import datetime

# 送信先URL（GitHubのSecretsに設定されているもの）
WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data(event_name=""):
    # 取得したい銘柄とYahoo Financeのシンボル
    symbols = {
        "USDJPY": "JPY=X",   # ドル円
        "ILS": "ILS=X",      # イスラエル・シェケル (USD/ILS)
        "Gold": "GC=F",      # 金先物
        "CrudeOil": "CL=F",   # 原油先物
        "S&P500": "^GSPC",    # S&P500
        "SOX": "^SOX",        # 半導体株指数
        "NaturalGas": "NG=F"  # 天然ガス
    }

    data_results = {}
    
    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            # 最新の終値を取得
            latest_data = ticker.history(period="1d")
            if not latest_data.empty:
                price = latest_data['Close'].iloc[-1]
                
                # ILSの場合は ILS/USD (1 ÷ USDILS) に変換
                if name == "ILS":
                    price = 1 / price
                
                data_results[name] = round(float(price), 4 if name == "ILS" else 2)
            else:
                data_results[name] = 0
        except Exception as e:
            print(f"エラー ({name}): {e}")
            data_results[name] = 0

    # 送信データの作成
    payload = {
        "sheetName": "MarketData",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "usdjpy": data_results.get("USDJPY"),
        "ils": data_results.get("ILS"),
        "gold": data_results.get("Gold"),
        "crudeoil": data_results.get("CrudeOil"),
        "sp500": data_results.get("S&P500"),
        "sox": data_results.get("SOX"),
        "gas": data_results.get("NaturalGas"),
        "event": event_name
    }

    # スプレッドシートへ送信
    try:
        response = requests.post(WEBAPP_URL, json=payload)
        if response.status_code == 200:
            print(f"市場データ送信成功: {response.status_code}")
            print(f"送信データ: {payload}")
        else:
            print(f"送信失敗: {response.status_code}")
    except Exception as e:
        print(f"通信エラー: {e}")

if __name__ == "__main__":
    get_market_data("定期更新")
