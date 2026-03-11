import os
import requests
import yfinance as yf
import time
import numpy as np

WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_historical_data():
    symbols = {
        "USDJPY": "JPY=X", "Gold": "GC=F", "CrudeOil": "CL=F",
        "S&P500": "^GSPC", "SOX": "^SOX", "NaturalGas": "NG=F"
    }
    
    # 過去180日分を取得
    data = yf.download(list(symbols.values()), period="180d", interval="1d")
    
    # 【重要】データがない日（休日など）を「前の日の値」で埋める
    data = data.ffill().replace({np.nan: 0})
    
    for date, row in data.iterrows():
        try:
            # データの抽出（yfinanceのマルチインデックス対応）
            payload = {
                "sheetName": "MarketData",
                "date": date.strftime("%Y-%m-%d"),
                "usdjpy": float(row['Close']['JPY=X']),
                "gold": float(row['Close']['GC=F']),
                "crudeoil": float(row['Close']['CL=F']),
                "sp500": float(row['Close']['^GSPC']),
                "sox": float(row['Close']['^SOX']),
                "gas": float(row['Close']['NG=F'])
            }
            
            # 送信
            res = requests.post(WEBAPP_URL, json=payload)
            print(f"{date.strftime('%Y-%m-%d')} 送信完了: {res.status_code}")
            time.sleep(0.3)
        except Exception as e:
            print(f"{date.strftime('%Y-%m-%d')} スキップ: {e}")

if __name__ == "__main__":
    get_historical_data()
