import streamlit as st
import google.generativeai as genai

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="핏코치 AI",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =========================
# Gemini 설정
# =========================
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
except Exception as e:
    st.error("Gemini API 설정 오류")
    st.error(str(e))
    st.stop()

# =========================
# 제목
# =========================
st.title("💪 핏코치 AI")
st.caption("다이어트 · 운동 · 식단 전문 AI 코치")

# =========================
# 사이드바
# =========================
with st.sidebar:
    st.header("⚙️ 메뉴")

    st.markdown("""
### 질문 예시
- 체지방 감량 운동 추천해줘
- 다이어트 식단 짜줘
- 홈트 루틴 만들어줘
- 단백질 얼마나 먹어야 해?
- 살 빼는 운동 알려줘
""")

    if st.button("🔄 대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요! 운동·식단 전문 AI 코치입니다. 무엇이 궁금한가요?"
            }
        ]
        st.rerun()

# =========================
# 세션 상태
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 💪\n\n"
                "저는 운동·식단 전문 AI 코치입니다.\n\n"
                "다이어트, 운동 루틴, 식단, 단백질 섭취 등에 대해 질문해보세요!"
            )
        }
    ]

# =========================
# 채팅 출력
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 사용자 입력
# =========================
user_input = st.chat_input("질문을 입력하세요...")

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("답변 생성 중..."):

            try:
                system_prompt = """
당신은 운동 및 영양 전문가입니다.

규칙:
- 운동, 다이어트, 체중감량, 식단 관련 질문에 답변한다.
- 초보자도 이해하기 쉽게 설명한다.
- 위험한 다이어트는 추천하지 않는다.
- 운동 루틴 요청 시 예시 루틴을 제공한다.
- 식단 요청 시 예시 식단을 제공한다.
- 답변은 친절하고 실용적으로 작성한다.
"""

                history_text = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "AI"
                    history_text += f"{role}: {msg['content']}\n"

                prompt = f"""
{system_prompt}

대화 기록:
{history_text}

사용자 질문:
{user_input}
"""

                response = model.generate_content(prompt)

                answer = response.text

            except Exception as e:
                answer = f"""
⚠️ 오류가 발생했습니다.

오류 내용:
{str(e)}
"""

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
