import streamlit as st
from datetime import datetime
import json
import os

# -----------------------------
# 설정
# -----------------------------
st.set_page_config(page_title="다이어트 PT 코치", page_icon="💪", layout="centered")

DATA_FILE = "data.json"

# -----------------------------
# 데이터 로드/저장
# -----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# -----------------------------
# 기본 초기화
# -----------------------------
if "logs" not in data:
    data["logs"] = []

# -----------------------------
# 사이드바 - 프로필
# -----------------------------
st.sidebar.title("🧍 프로필 설정")

goal = st.sidebar.selectbox("목표", ["감량", "유지", "증량"])
height = st.sidebar.number_input("키 (cm)", 140, 220, 170)
weight = st.sidebar.number_input("몸무게 (kg)", 30, 200, 70)
age = st.sidebar.number_input("나이", 10, 100, 25)

activity = st.sidebar.selectbox(
    "활동량",
    ["낮음", "보통", "높음"]
)

# 간단 TDEE 계산
def calc_target_calories():
    base = weight * 22
    if activity == "낮음":
        base *= 1.2
    elif activity == "보통":
        base *= 1.4
    else:
        base *= 1.6

    if goal == "감량":
        base -= 400
    elif goal == "증량":
        base += 300

    return int(base)

target_cal = calc_target_calories()

st.sidebar.markdown(f"🔥 목표 칼로리: **{target_cal} kcal**")

# -----------------------------
# 제목
# -----------------------------
st.title("💪 다이어트 PT 코치 봇")
st.caption("식단 + 운동 + AI 코칭")

# -----------------------------
# 입력
# -----------------------------
st.subheader("🍽️ 식단 기록")

meal = st.text_input("오늘 먹은 음식 (예: 김밥, 치킨)")
meal_cal = st.number_input("칼로리 (모르면 대략 입력)", 0, 3000, 500)

st.subheader("🏃 운동 기록")

exercise = st.text_input("운동 종류 (예: 걷기, 헬스)")
exercise_time = st.number_input("운동 시간 (분)", 0, 300, 30)

# -----------------------------
# 저장 버튼
# -----------------------------
if st.button("저장하기"):
    entry = {
        "time": str(datetime.now()),
        "meal": meal,
        "meal_cal": meal_cal,
        "exercise": exercise,
        "exercise_time": exercise_time
    }

    data["logs"].append(entry)
    save_data(data)
    st.success("저장 완료!")

# -----------------------------
# 분석
# -----------------------------
st.divider()
st.subheader("📊 오늘 분석")

today_logs = data["logs"][-10:]  # 최근 데이터

total_cal = sum([x["meal_cal"] for x in today_logs])
total_ex = sum([x["exercise_time"] for x in today_logs])

burned = total_ex * 5  # 단순 계산

st.write(f"섭취 칼로리: {total_cal} kcal")
st.write(f"운동 시간: {total_ex} 분")
st.write(f"추정 소모: {burned} kcal")

balance = total_cal - burned

if balance > target_cal:
    st.error("⚠️ 목표 초과! 식단 조절 필요")
elif balance < target_cal - 500:
    st.warning("⚠️ 너무 적게 먹고 있음")
else:
    st.success("👍 좋은 균형입니다!")

# -----------------------------
# PT 코칭 메시지
# -----------------------------
st.divider()
st.subheader("🧠 PT 코치 메시지")

if balance > target_cal:
    msg = "오늘은 조금 과식했어요. 내일은 탄수화물 줄이고 단백질 늘려보세요!"
elif total_ex == 0:
    msg = "운동이 부족합니다. 20분이라도 걷기부터 시작해보세요!"
else:
    msg = "좋은 페이스입니다! 꾸준함이 가장 중요합니다 💪"

st.info(msg)

# -----------------------------
# 기록 보기
# -----------------------------
st.divider()
st.subheader("📜 기록")

for i, log in enumerate(reversed(data["logs"][-5:])):
    st.write(f"""
    **{log['time']}**
    - 음식: {log['meal']} ({log['meal_cal']} kcal)
    - 운동: {log['exercise']} ({log['exercise_time']} 분)
    """)
