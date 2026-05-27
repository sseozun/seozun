import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 상담 챗봇")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 😊 연애 고민을 편하게 이야기해 주세요!"
        }
    ]

# 기존 채팅 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            try:
                # 대화 기록 구성
                history = []

                for msg in st.session_state.messages:
                    role = "model" if msg["role"] == "assistant" else "user"

                    history.append(
                        types.Content(
                            role=role,
                            parts=[types.Part(text=msg["content"])]
                        )
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=history,
                    config=types.GenerateContentConfig(
                        system_instruction="""
                        너는 공감 능력이 뛰어난 연애상담 챗봇이다.
                        사용자의 고민을 진심으로 들어주고,
                        따뜻하고 현실적인 조언을 제공해라.
                        공격적이거나 판단적인 말투는 사용하지 마라.
                        """,
                        temperature=0.8,
                        max_output_tokens=1024,
                    )
                )

                assistant_reply = response.text

                st.markdown(assistant_reply)

                # 응답 저장
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_reply
                    }
                )

            except Exception as e:
                error_message = f"❌ 오류가 발생했습니다: {e}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")

    if st.button("채팅 기록 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요 😊 연애 고민을 편하게 이야기해 주세요!"
            }
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("### 사용 모델")
    st.code("gemini-2.5-flash-lite")
