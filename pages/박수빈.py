import streamlit as st
import pandas as pd
from datetime import date, timedelta
import random

# ------------------
# 페이지 설정
# ------------------
st.set_page_config(
    page_title="다이어트 플래너 봇",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 다이어트 플래너 봇")
st.write("건강한 식단과 운동 계획을 확인해보세요!")

# ------------------
# 다이어트 팁
# ------------------
tips = [
    "물을 하루 2L 이상 마셔보세요.",
    "식사 전에 물 한 컵을 마시면 과식을 줄일 수 있습니다.",
    "단백질 섭취를 늘리면 포만감이 오래갑니다.",
    "충분한 수면은 다이어트에 매우 중요합니다.",
    "하루 30분 걷기만 해도 건강에 도움이 됩니다."
]

st.info("💡 오늘의 팁: " + random.choice(tips))

# ------------------
# BMI 계산기
# ------------------
st.header("📊 BMI 계산기")

col1, col2 = st.columns(2)

with col1:
    height = st.number_input(
        "키(cm)",
        min_value=100,
        max_value=250,
        value=170
    )

with col2:
    weight = st.number_input(
        "몸무게(kg)",
        min_value=20,
        max_value=300,
        value=65
    )

if height > 0:
    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        state = "저체중"
    elif bmi < 23:
        state = "정상"
    elif bmi < 25:
        state = "과체중"
    else:
        state = "비만"

    st.success(f"BMI: {bmi:.1f} ({state})")

# ------------------
# 목표 체중
# ------------------
st.header("🎯 목표 체중")

goal_weight = st.number_input(
    "목표 체중(kg)",
    min_value=20,
    max_value=300,
    value=60
)

remain = weight - goal_weight

if remain > 0:
    st.warning(f"목표까지 {remain:.1f}kg 남았습니다.")
elif remain == 0:
    st.success("목표 체중을 달성했습니다!")
else:
    st.info(f"현재 목표보다 {-remain:.1f}kg 적습니다.")

# ------------------
# 30일 계획 생성
# ------------------
st.header("📅 식단 · 운동 일정")

meal_plan = [
    "닭가슴살 샐러드",
    "현미밥 + 계란",
    "고구마 + 닭가슴살",
    "연어 샐러드",
    "그릭요거트 + 과일",
    "두부 샐러드",
    "현미김밥"
]

exercise_plan = [
    "걷기 30분",
    "러닝 20분",
    "홈트 30분",
    "근력운동 40분",
    "자전거 30분",
    "스트레칭 20분",
    "휴식"
]

today = date.today()

schedule = []

for i in range(30):
    current_day = today + timedelta(days=i)

    schedule.append(
        {
            "날짜": current_day.strftime("%Y-%m-%d"),
            "식단": meal_plan[i % len(meal_plan)],
            "운동": exercise_plan[i % len(exercise_plan)]
        }
    )

df = pd.DataFrame(schedule)

selected_date = st.selectbox(
    "날짜 선택",
    df["날짜"]
)

selected_row = df[df["날짜"] == selected_date]

if len(selected_row) > 0:
    st.subheader("선택한 날짜 계획")

    st.write(
        "🍽️ 식단:",
        selected_row.iloc[0]["식단"]
    )

    st.write(
        "🏃 운동:",
        selected_row.iloc[0]["운동"]
    )

st.subheader("30일 일정표")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ------------------
# 물 섭취 체크
# ------------------
st.header("💧 물 섭취 체크")

water = st.slider(
    "오늘 마신 물(L)",
    0.0,
    5.0,
    2.0,
    0.1
)

if water >= 2:
    st.success("좋아요! 충분한 수분을 섭취했습니다.")
else:
    st.warning("물을 조금 더 마셔보세요.")

# ------------------
# 운동 체크
# ------------------
st.header("✅ 오늘 운동 완료")

done = st.checkbox("오늘 운동을 완료했습니다.")

if done:
    st.balloons()
    st.success("훌륭합니다! 꾸준함이 성공의 비결입니다.")

st.markdown("---")
st.caption("Diet Planner Bot")
