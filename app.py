import streamlit as st
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY") 
)

# ==========================================
# 1. 関数の定義
# ==========================================
def get_expert_response(user_input: str, expert_role: str) -> str:
    """
    入力テキストと選択された専門家の種類を受け取り、LLMからの回答を返す関数。
    """
    # LLMの初期化（ここではOpenAIのモデルを使用）
    # ※ 実行には環境変数 OPENAI_API_KEY が設定されている必要があります
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # 選択された専門家に応じてシステムメッセージを変更
    if expert_role == "🏋️‍♂️ パーソナルトレーナー":
        system_message = (
            "あなたはプロのパーソナルトレーナーです。"
            "筋トレ、ダイエット、健康管理などの質問に対して、"
            "科学的根拠に基づきつつ、相手のモチベーションが上がるような元気でポジティブなアドバイスをしてください。"
        )
    else:  # 💰 ファイナンシャルプランナー
        system_message = (
            "あなたは経験豊富なファイナンシャルプランナーです。"
            "家計管理、節約、資産運用などの質問に対して、"
            "リスクを考慮した上で、堅実で論理的、かつ具体的なアドバイスをプロフェッショナルなトーンで提供してください。"
        )
        
    # プロンプトテンプレートの作成
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}")
    ])
    
    # チェーンの作成と実行
    chain = prompt | llm
    response = chain.invoke({"input": user_input})
    
    return response.content

# ==========================================
# 2. WebアプリのUI構築 (Streamlit)
# ==========================================
# ページのタイトル
st.set_page_config(page_title="お悩み相談AIアプリ", page_icon="💡")
st.title("💡 お悩み相談AIアプリ")

# 概要と操作方法の説明
st.markdown("""
### アプリの概要
このアプリは、あなたの悩みに合わせて2種類の「専門家AI」が回答してくれる相談アプリです。
健康や体づくりについては**パーソナルトレーナー**に、お金や家計については**ファイナンシャルプランナー**に相談してみましょう！

### 操作方法
1. 下記のラジオボタンから、相談したい専門家を選択してください。
2. 相談内容を入力フォームに書き込んでください。
3. 「相談する」ボタンを押すと、専門家AIからの回答が表示されます。
---
""")

# ラジオボタンで専門家を選択
selected_role = st.radio(
    "相談する専門家を選んでください：",
    ("🏋️‍♂️ パーソナルトレーナー", "💰 ファイナンシャルプランナー")
)

# 入力フォームの作成
with st.form(key="consultation_form"):
    user_input = st.text_area("相談内容を入力してください：", placeholder="例：最近太り気味で... / 毎月のお小遣いを節約するには...")
    submit_button = st.form_submit_button(label="相談する")

# ==========================================
# 3. 処理と結果の表示
# ==========================================
# 送信ボタンが押され、かつテキストが入力されている場合
if submit_button:
    if user_input.strip() == "":
        st.warning("相談内容を入力してください。")
    else:
        with st.spinner(f"{selected_role} が回答を考えています..."):
            try:
                # 定義した関数を呼び出して回答を取得
                answer = get_expert_response(user_input, selected_role)
                
                # 回答の表示
                st.success("回答が届きました！")
                st.markdown(f"**{selected_role}からのアドバイス：**")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました。APIキーの設定などをご確認ください。\n詳細: {e}")




