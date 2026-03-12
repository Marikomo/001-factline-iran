import os
import requests
import yfinance as yf
from datetime import datetime

# 送信先URL (GitHubのSecretsから読み込み)
WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data(event_name="なし"):
    """
    Yahoo Financeから市場データを取得し、スプレッドシートへ送信する。
    main.pyからAI要約（event_name）を受け取って、I列に書き込みます。
    """
    
    # 取得したい銘柄のリスト
    symbols = {
        "USDJPY": "JPY=X",
        "ILS": "ILS=X",      # イスラエル・シェケル
        "Gold": "GC=F",
        "CrudeOil": "CL=F",
        "S&P500": "^GSPC",
        "SOX": "^SOX",
        "NaturalGas": "NG=F"
    }
    
    results = {"date": datetime.now().strftime("%Y-%m-%d %H:%M")}

    print("市場データを取得中...")
    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            # 最新の価格を取得（fast_info['last_price'] を使用）
            price = ticker.fast_info['last_price']
            results[name] = round(price, 2)
        except Exception as e:
            print(f"{name} の取得に失敗: {e}")
            results[name] = "" # 失敗時は空文字

    # スプレッドシートへ送るデータ
    # ※ここで event_name を payload に入れています
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
        "event": event_name  # AIからの要約テキストをセット
    }

    # Google Apps Script(GAS)へ送信
    try:
        print(f"送信データ: {payload}")
        res = requests.post(WEBAPP_URL, json=payload)
        print(f"市場データ送信成功: {res.status_code}")
    except Exception as e:
        print(f"送信エラー発生: {e}")

if __name__ == "__main__":
    # 単体で実行した場合のテスト用
    get_market_data("テスト実行（main.pyを経由していません）")
