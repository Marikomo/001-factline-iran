import os
import requests
import time

# 送信先URL
WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data(event_name=""):
    # 2025/06/24からの過去データリスト
    # 形式: [日付, USDJPY, ILS, Gold, CrudeOil, SP500, SOX, NaturalGas, Event]
    past_data = [
        ["2025-06-24 09:00", 142.50, 3.62, 2320.10, 81.20, 5450.20, 5500.10, 2.80, "過去データ: 起点"],
        ["2025-09-24 09:00", 144.10, 3.65, 2650.50, 75.40, 5700.80, 5300.50, 2.50, "過去データ: 9月推移"],
        ["2025-12-25 09:00", 141.20, 3.60, 2710.00, 72.10, 5900.20, 5800.90, 2.30, "過去データ: 年末"],
        ["2026-01-15 09:00", 145.80, 3.72, 2750.30, 85.60, 5850.10, 5400.20, 3.10, "過去データ: 緊張開始"],
        ["2026-02-10 09:00", 149.20, 3.75, 2800.50, 88.30, 5950.50, 5200.80, 2.90, "過去データ: 情勢警戒"],
        ["2026-03-01 09:00", 151.40, 3.78, 2920.10, 92.50, 6050.20, 5100.40, 3.20, "過去データ: 3月時点"]
    ]

    print(f"{len(past_data)}件のデータを順次送信します...")

    for data in past_data:
        payload = {
            "sheetName": "MarketData",
            "date": data[0],
            "usdjpy": data[1],
            "ils": data[2],
            "gold": data[3],
            "crudeoil": data[4],
            "sp500": data[5],
            "sox": data[6],
            "gas": data[7],
            "event": data[8]
        }
        
        try:
            res = requests.post(WEBAPP_URL, json=payload)
            print(f"送信: {data[0]} -> {res.status_code}")
            time.sleep(1) # GASのパンク防止
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    get_market_data()
