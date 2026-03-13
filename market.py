import yfinance as yf
import pandas as pd

def export_ils_for_copy():
    print("データを取得中...少々お待ちください。")
    
    # 2025-06-24から2026-03-11までのILSデータを取得
    # yfinanceは自動で土日を除いた「市場営業日」のみを抽出します
    df = yf.download("ILS=X", start="2025-06-24", end="2026-03-12")

    if df.empty:
        print("データが取得できませんでした。")
        return

    print("\n--- 以下のデータをコピーして、スプレッドシートのA列とC列付近に貼り付けてください ---\n")
    print("日付\tILS(USD/ILS)") # タブ区切り
    
    for d in df.index:
        date_str = d.strftime("%Y/%m/%d")
        # yfinanceの新しい仕様に合わせて価格を抽出
        try:
            price = float(df.loc[d, 'Close'])
            # スプレッドシートに貼り付けやすいように「日付(タブ)価格」の形式で出力
            print(f"{date_str}\t{round(price, 4)}")
        except:
            continue
    
    print("\n--- データの終わり ---")

if __name__ == "__main__":
    export_ils_for_copy()
