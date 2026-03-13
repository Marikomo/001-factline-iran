import yfinance as yf

def force_show_all_ils():
    print("--- データの強制取得を開始します ---")
    
    # 銘柄: USD/ILS (イスラエル・シェケル)
    symbol = "ILS=X"
    
    # 期間を start/end で指定し、さらに interval='1d' (日足) を明示します
    ticker = yf.Ticker(symbol)
    df = ticker.history(start="2025-06-24", end="2026-03-13", interval="1d")

    if df.empty:
        print("データが空です。期間指定を1ヶ月ずつに分割して試行します...")
        # 万が一空だった場合の予備手段（直近1年分をまるごと取る）
        df = ticker.history(period="1y")

    print(f"取得件数: {len(df)} 件")
    print("\n【ここからコピーしてください】")
    print("日付\tILSレート")
    
    for index, row in df.iterrows():
        # 土日を除いた平日のデータが1行ずつ出力されます
        date_str = index.strftime('%Y/%m/%d')
        price = round(float(row['Close']), 4)
        print(f"{date_str}\t{price}")
    
    print("【ここまで】\n")
    print("--- 出力完了 ---")

if __name__ == "__main__":
    force_show_all_ils()
