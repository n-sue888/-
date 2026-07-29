import streamlit as st
from openai import OpenAI

st.title("🗣️ AI英会話パートナー")

# APIキーの設定（StreamlitのSecrets機能や入力フォームから取得）
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    # 履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a friendly English tutor. Chat with the user in English. "
                    "If the user makes a grammar mistake or awkward phrasing, "
                    "gently correct it at the end of your response in Japanese."
                )
            }
        ]

    # チャット履歴の描画
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # ユーザー入力
    if user_input := st.chat_input("英語で話しかけてみよう（例: Hello! How are you?）"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # AIの応答生成
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            ai_reply = response.choices[0].message.content
            st.write(ai_reply)

        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
else:
    st.warning("サイドバーに OpenAI API Key を入力してください。")
