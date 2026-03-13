import yfinance as yf

def export_for_manual_copy():
    print("--- 過去データ抽出開始 (2025/06/24 - 2026/03/11) ---")
    
    # ILS（シェケル）のデータを取得
    ticker = yf.Ticker("ILS=X")
    # 土日を除く全日程を強制取得
    df = ticker.history(start="2025-06-24", end="2026-03-12", interval="1d")

    if df.empty:
        print("データが取得できませんでした。期間を広げて再試行します。")
        df = ticker.history(period="1y")

    print("\n【ここから下をコピーしてスプレッドシートに貼り付けてください】")
    print("日付\tILS(シェケル)") # タブ区切り

    for index, row in df.iterrows():
        date_str = index.strftime('%Y/%m/%d')
        price = round(float(row['Close']), 4)
        # 1行ずつ文字として出力
        print(f"{date_str}\t{price}")
    
    print("【コピー範囲の終わり】\n")

if __name__ == "__main__":
    export_for_manual_copy()
