import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="나만의 AI 다이어트 영양사",
    page_icon="🥗",
    layout="centered"
)

# 깔끔한 타이틀 바 구현
st.title("🥗 나만의 AI 다이어트 영양사")
st.caption("당신의 신체 정보와 목표에 딱 맞춘 하루 다이어트 식단을 제안합니다.")
st.markdown("---")

# 2. Streamlit Secrets로부터 API 키 불러오기 및 클라이언트 초기화
# 초보자가 배포 시 API 키 누락으로 인한 에러를 방지하기 위한 예외 처리
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 **API Key 누락:** Streamlit Cloud 설정(Advanced Settings)에서 `GEMINI_API_KEY`를 등록해주세요.")
    st.stop()

# 정석대로 google-genai 라이브러리의 클라이언트 초기화
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 사용자 입력 양식 (UI/UX 차별화: 직관적인 사이드바와 메인 폼 구성)
st.subheader("📋 나의 신체 정보 및 목표 입력")

with st.form("diet_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender = st.selectbox("성별", ["선택 안함", "남성", "여성"])
    with col2:
        age = st.number_input("나이 (세)", min_value=10, max_value=100, value=25, step=1)
    with col3:
        activity = st.selectbox(
            "평소 활동량", 
            ["매우 적음 (좌식 생활)", "보통 (주 1~3회 운동)", "많음 (주 4회 이상 운동)"]
        )
        
    col4, col5 = st.columns(2)
    with col4:
        height = st.number_input("키 (cm)", min_value=100.0, max_value=250.0, value=165.0, step=0.1)
    with col5:
        weight = st.number_input("현재 체중 (kg)", min_value=30.0, max_value=200.0, value=60.0, step=0.1)
        
    diet_goal = st.radio(
        "🎯 다이어트 목표",
        ["체중 감량 (건강하게 살 빼기)", "린매스업 (체지방 줄이고 근육 키우기)", "바디프로필 준비 (강한 식단 통제)"],
        horizontal=True
    )
    
    allergy = st.text_input("⚠️ 알레르기 또는 기피 음식을 입력해주세요 (예: 오이, 우유, 없음)", value="없음")
    
    # 제출 버튼
    submitted = st.form_submit_with_button("🥗 맞춤형 식단 생성하기")

# 4. 비즈니스 로직 및 AI 스트리밍 응답 구현
if submitted:
    if gender == "선택 안함":
        st.warning("⚠️ 성별을 정확히 선택해 주세요.")
    else:
        # 프롬프트 엔지니어링: 일관성 있고 깔끔한 가독성을 위한 구조화 요청
        prompt = f"""
        당신은 전문 스포츠 영양사이자 다이어트 전문가입니다. 아래 사용자 정보를 바탕으로 칼로리와 영양소(탄단지)를 고려한 맞춤형 하루 다이어트 식단을 짜주세요.

        [사용자 정보]
        - 성별: {gender}
        - 나이: {age}세
        - 키: {height}cm
        - 현재 체중: {weight}kg
        - 평소 활동량: {activity}
        - 다이어트 목표: {diet_goal}
        - 알레르기 및 기피 음식: {allergy}

        [출력 요구사항]
        1. 하루 권장 총 섭취 칼로리와 탄수화물/단백질/지방 대략적인 목표 비율을 먼저 제시해 주세요.
        2. 아침, 점심, 간식, 저녁으로 나누어 구체적인 식단 메뉴와 간단한 이유를 표(Table)나 깔끔한 글머리 기호로 작성해 주세요.
        3. 이 목표를 달성하기 위한 영양사로서의 핵심 팁 2가지를 마지막에 포함해 주세요.
        4. 친절하고 격려하는 말투를 사용해 주세요.
        """
        
        st.markdown("---")
        st.subheader("✨ AI 추천 맞춤형 식단 결과")
        
        # 사용자 경험을 극대화하기 위한 스트리밍(Streaming) 출력 구현
        status_placeholder = st.empty()
        response_placeholder = st.empty()
        
        status_placeholder.info("🤖 AI 영양사가 식단을 분석하고 짜는 중입니다... 잠시만 기다려 주세요.")
        
        try:
            # gemini-2.5-flash-lite 모델 및 generate_content_stream 사용
            response_stream = client.models.generate_content_stream(
                model='gemini-2.5-flash-lite',
                contents=prompt
            )
            
            full_response = ""
            for chunk in response_stream:
                full_response += chunk.text
                # 글이 작성되는 대로 실시간으로 화면에 출력
                response_placeholder.markdown(full_response)
                
            status_placeholder.success("✅ 식단 생성이 완료되었습니다! 오늘부터 시작해 볼까요?")
            
        except APIError as e:
            status_placeholder.empty()
            st.error(f"❌ Gemini API 에러가 발생했습니다: {e}")
        except Exception as e:
            status_placeholder.empty()
            st.error(f"❌ 예기치 못한 에러가 발생했습니다: {e}")

# 5. 하단 푸터 설정
st.markdown("---")
st.caption("© 2026 AI Diet Planner. Powered by Gemini 2.5 Flash Lite.")
