import os
import requests
import yfinance as yf
import time

WEBAPP_URL = os.getenv("WEBAPP_URL")

def get_market_data(event_name="ILS全日程インポート"):
    print("2025-06-24から2026-03-11までのILS（シェケル）データを取得中...")
    
    # ILS=X (USD/ILS) の全期間データを取得
    # yfinanceが自動で土日を除いた市場営業日のデータを返します
    ils_df = yf.download("ILS=X", start="2025-06-24", end="2026-03-12")

    if ils_df.empty:
        print("データの取得に失敗しました。")
        return

    # 日付リストを取得
    dates = ils_df.index
    print(f"合計 {len(dates)} 日分のデータを送信します。少々お待ちください...")

    for d in dates:
        date_str = d.strftime("%Y-%m-%d")
        
        # その日の終値（Close）を取得
        # ※ yfinanceの仕様変更に対応するためfloatに変換
        try:
            ils_price = float(ils_df.loc[d, 'Close'])
        except:
            continue

        payload = {
            "sheetName": "MarketData",
            "date": date_str,
            "usdjpy": 0,    # 今回はILSのみを目的とするため他は0
            "ils": round(ils_price, 4), # 単位は USD/ILS
            "gold": 0,
            "crudeoil": 0,
            "sp500": 0,
            "sox": 0,
            "gas": 0,
            "event": "過去データ一括投入"
        }

        try:
            res = requests.post(WEBAPP_URL, json=payload, timeout=10)
            print(f"送信完了: {date_str} -> {ils_price:.4f} ({res.status_code})")
            # 大量送信によるGASの制限を避けるため少し待機
            time.sleep(0.3)
        except Exception as e:
            print(f"エラー ({date_str}): {e}")

if __name__ == "__main__":
    get_market_data()
