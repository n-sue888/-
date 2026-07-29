import streamlit as st
from google import genai
from google.genai import types

st.title("🗣️ AI英会話パートナー (Gemini)")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # チャット履歴の描画
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ユーザー入力
    if user_input := st.chat_input("英語で話しかけてみよう（例: Hello! How are you?）"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # API送信用に履歴を Content オブジェクトに変換
        contents = []
        for m in st.session_state.messages:
            role = "user" if m["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=m["content"])]
                )
            )

        # Geminiへの送信と応答表示
        with st.chat_message("assistant"):
            config = types.GenerateContentConfig(
                system_instruction=(
                    "You are a friendly English tutor. Chat with the user in English. "
                    "If the user makes a grammar mistake or awkward phrasing, "
                    "gently correct it at the end of your response in Japanese."
                )
            )
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config
            )
            
            ai_reply = response.text
            st.write(ai_reply)

        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
else:
    st.warning("サイドバーに Gemini API Key を入力してください。")
