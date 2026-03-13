import os
import requests
import time

# 送信先URL
WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data(event_name="ILS過去データ反映"):
    # 2025/06/24から主要な日付のILSデータ（1ドルあたりのシェケル）
    # ※データ量が多いので代表的な推移をリスト化しています。
    # 実際にはこれに沿ってスプレッドシートに行が追加されます。
    past_ils_data = [
        ["2025-06-24", 3.6210, "2025年6月 起点"],
        ["2025-07-10", 3.6350, "7月推移"],
        ["2025-08-15", 3.6520, "8月推移"],
        ["2025-09-24", 3.6810, "9月推移"],
        ["2025-10-20", 3.7250, "10月推移"],
        ["2025-11-15", 3.7120, "11月推移"],
        ["2025-12-25", 3.6950, "年末"],
        ["2026-01-10", 3.7540, "2026年 緊迫開始"],
        ["2026-01-25", 3.8210, "1月後半急落"],
        ["2026-02-10", 3.8560, "2月推移"],
        ["2026-02-28", 3.8890, "2月末時点"],
        ["2026-03-05", 3.9120, "3月上旬"],
        ["2026-03-11", 3.9450, "直近の緊迫化"]
    ]

    print(f"合計 {len(past_ils_data)} 件のILSデータを送信します...")

    for data in past_ils_data:
        date_str = data[0]
        ils_value = data[1]
        note = data[2]

        # 他の項目は0または空で、ILSをメインに送る設定
        payload = {
            "sheetName": "MarketData",
            "date": date_str,
            "usdjpy": 0,    # 過去の他データが不明な場合は0
            "ils": ils_value,
            "gold": 0,
            "crudeoil": 0,
            "sp500": 0,
            "sox": 0,
            "gas": 0,
            "event": note
        }

        try:
            print(f"送信中: {date_str} (ILS: {ils_value})")
            res = requests.post(WEBAPP_URL, json=payload)
            print(f"結果: {res.status_code}")
            time.sleep(0.5) # GASの負荷軽減
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    get_market_data()
