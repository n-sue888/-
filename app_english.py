import streamlit as st
from google import genai
from google.genai import types

st.title("🗣️ AI英会話パートナー (Gemini)")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    # 画面が再描画されてもチャットセッションを維持する
    if "chat" not in st.session_state:
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            system_instruction=(
                "You are a friendly English tutor. Chat with the user in English. "
                "If the user makes a grammar mistake or awkward phrasing, "
                "gently correct it at the end of your response in Japanese."
            )
        )
        st.session_state.chat = client.chats.create(
            model="gemini-2.0-flash",
            config=config
        )
        st.session_state.messages = []

    # 過去のメッセージを表示
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ユーザー入力
    if user_input := st.chat_input("英語で話しかけてみよう（例: Hello! How are you?）"):
        # ユーザーの発言を表示＆保存
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Geminiへ送信（chats 機能を使用）
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(user_input)
            ai_reply = response.text
            st.write(ai_reply)

        # AIの発言を保存
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
else:
    st.warning("サイドバーに Gemini API Key を入力してください。")
