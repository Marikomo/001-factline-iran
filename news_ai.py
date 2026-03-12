import os
import google.generativeai as genai

# GeminiのAPIキーを設定
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

def get_event_summary():
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # AIにニュースの調査と要約を依頼するプロンプト
        prompt = """
        あなたは地政学リスクの専門家です。現在、イラン、イスラエルを中心とした中東情勢の最新ニュースを確認し、
        テキサスで生活する人が「ガソリン価格への影響」を判断するための重要なトピックを1つ、
        30文字以内で短く要約してください。
        
        もし特に大きな動きがない場合は「大きな政情変化なし」と答えてください。
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"AI要約エラー: {e}")
        return "ニュース取得エラー"

if __name__ == "__main__":
    print(get_event_summary())
