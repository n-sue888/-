import streamlit as st
from google import genai

st.title("🗣️ AI英会話パートナー (Gemini)")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)

    # 履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 過去の会話を表示
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ユーザー入力
    if user_input := st.chat_input("英語で話しかけてみよう（例: Hello! How are you?）"):
        # ユーザーの発言を表示＆保存
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # AIの返答取得
        with st.chat_message("assistant"):
            prompt = (
                "You are a friendly English tutor. Chat with the user in English. "
                "If the user makes a grammar mistake or awkward phrasing, "
                "gently correct it at the end of your response in Japanese.\n\n"
                f"User: {user_input}"
            )
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            ai_reply = response.text
            st.write(ai_reply)

        # AIの返答を保存
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
else:
    st.warning("サイドバーに Gemini API Key を入力してください。")
