import streamlit as st
from google import genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="핏코치 AI",
    page_icon="💪",
    layout="centered"
)

st.title("💪 핏코치 AI")
st.caption("다이어트 · 운동 · 식단 전문 AI 코치")

# -----------------------------
# API 키 확인
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -----------------------------
# Gemini 클라이언트
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Gemini 클라이언트 생성 실패")
    st.stop()

# -----------------------------
# 세션 상태
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 💪\n\n"
                "저는 다이어트 운동·식단 전문 AI 코치입니다.\n\n"
                "운동 루틴, 식단, 체중 감량, 근육 증가 등에 대해 질문해보세요!"
            )
        }
    ]

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("⚙️ 메뉴")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "대화가 초기화되었습니다.\n\n"
                    "운동이나 식단에 대해 질문해보세요!"
                )
            }
        ]
        st.rerun()

    st.markdown("---")
    st.info(
        "예시 질문\n\n"
        "- 체지방 감량 운동 추천\n"
        "- 단백질 식단 짜줘\n"
        "- 홈트 루틴 만들어줘\n"
        "- 다이어트 중 간식 추천"
    )

# -----------------------------
# 채팅 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input(
    "운동, 식단, 다이어트에 대해 질문하세요..."
)

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
        with st.spinner("AI 코치가 답변 작성 중..."):

            try:
                system_prompt = """
당신은 전문 피트니스 코치이자 영양사입니다.

규칙:
- 운동, 식단, 체중 감량, 근육 증가 관련 질문에 친절하게 답변한다.
- 초보자도 이해하기 쉽게 설명한다.
- 위험한 다이어트 방법은 권장하지 않는다.
- 답변은 실용적으로 작성한다.
- 운동 루틴이 필요하면 예시 루틴을 제공한다.
- 식단 질문이면 식단 예시를 제공한다.
"""

                conversation = system_prompt + "\n\n"

                for msg in st.session_state.messages:
                    role = msg["role"]
                    content = msg["content"]

                    if role == "user":
                        conversation += f"사용자: {content}\n"
                    elif role == "assistant":
                        conversation += f"AI: {content}\n"

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=conversation
                )

                answer = response.text

            except Exception as e:
                answer = (
                    "죄송합니다. 현재 AI 응답 생성 중 오류가 발생했습니다.\n\n"
                    f"오류 내용: {str(e)}"
                )

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
