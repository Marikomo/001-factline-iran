import os
import requests
import yfinance as yf
import time

WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_historical_data():
    # 銘柄リスト
    symbols = {
        "USDJPY": "JPY=X", "Gold": "GC=F", "CrudeOil": "CL=F",
        "S&P500": "^GSPC", "SOX": "^SOX", "NaturalGas": "NG=F"
    }
    
    # 過去180日分を取得
    data = yf.download(list(symbols.values()), period="180d", interval="1d")
    
    # データを1日ずつスプレッドシートに飛ばす
    for date, row in data.iterrows():
        payload = {
            "sheetName": "MarketData",
            "date": date.strftime("%Y-%m-%d"),
            "usdjpy": round(row['Close']['JPY=X'], 2),
            "gold": round(row['Close']['GC=F'], 2),
            "crudeoil": round(row['Close']['CL=F'], 2),
            "sp500": round(row['Close']['^GSPC'], 2),
            "sox": round(row['Close']['^SOX'], 2),
            "gas": round(row['Close']['NG=F'], 2)
        }
        # 連続で送るとエラーになることがあるので、少し待つ
        requests.post(WEBAPP_URL, json=payload)
        print(f"{date.strftime('%Y-%m-%d')} 送信完了")
        time.sleep(0.5)

if __name__ == "__main__":
    get_historical_data()
