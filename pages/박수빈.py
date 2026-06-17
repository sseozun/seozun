import streamlit as st
import pandas as pd
from datetime import date, timedelta
import random

st.set_page_config(
    page_title="다이어트 플래너 봇",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 다이어트 플래너 봇")
st.caption("식단과 운동 계획을 한눈에 확인하세요!")

# -----------------------------
# 다이어트 팁
# -----------------------------
tips = [
    "물을 하루 2L 이상 마셔보세요.",
    "엘리베이터 대신 계단을 이용해보세요.",
    "식사 전 물 한 컵은 과식을 줄이는 데 도움이 됩니다.",
    "잠을 충분히 자는 것도 다이어트의 핵심입니다.",
    "단백질 섭취를 늘리면 포만감이 오래갑니다."
]

st.info(f"💡 오늘의 다이어트 팁 : {random.choice(tips)}")

# -----------------------------
# BMI 계산기
# -----------------------------
st.header("📊 BMI 계산기")

col1, col2 = st.columns(2)

with col1:
    height = st.number_input(
        "키(cm)",
        min_value=100.0,
        max_value=250.0,
        value=170.0
    )

with col2:
    weight = st.number_input(
        "몸무게(kg)",
        min_value=20.0,
        max_value=300.0,
        value=65.0
    )

try:
    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        result = "저체중"
    elif bmi < 23:
        result = "정상"
    elif bmi < 25:
        result = "과체중"
    else:
        result = "비만"

    st.success(f"BMI : {bmi:.1f} ({result})")

except:
    st.error("BMI 계산 중 오류가 발생했습니다.")

# -----------------------------
# 식단/운동 일정 생성
# -----------------------------
st.header("📅 식단 & 운동 일정 달력")

today = date.today()

meal_cycle = [
    "닭가슴살 샐러드",
    "현미밥 + 계란",
    "연어 샐러드",
    "고구마 + 닭가슴살",
    "그릭요거트 + 과일",
    "두부 샐러드",
    "현미김밥"
]

exercise_cycle = [
    "걷기 30분",
    "러닝 20분",
    "홈트 30분",
    "근력운동 40분",
    "자전거 30분",
    "스트레칭 20분",
    "휴식"
]

schedule = []

for i in range(30):
    day = today + timedelta(days=i)

    schedule.append({
        "날짜": day,
        "식단": meal_cycle[i % len(meal_cycle)],
        "운동": exercise_cycle[i % len(exercise_cycle)]
    })

df = pd.DataFrame(schedule)

selected_date = st.date_input(
    "날짜 선택",
    today
)

selected_row = df[df["날짜"] == pd.to_datetime(selected_date).date()]

if not selected_row.empty:
    st.subheader("선택한 날짜 계획")

    st.write(
        f"🍽️ 식단 : {selected_row.iloc[0]['식단']}"
    )

    st.write(
        f"🏃 운동 : {selected_row.iloc[0]['운동']}"
    )

st.subheader("30일 다이어트 일정")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# 진행 안내
# -----------------------------
st.header("🎯 다이어트 성공 습관")

st.markdown("""
- 하루 2L 물 마시기
- 야식 줄이기
- 주 3회 이상 운동
- 단백질 충분히 섭취
- 충분한 수면 유지
""")

st.success("꾸준함이 최고의 다이어트 비결입니다! 💪")1
