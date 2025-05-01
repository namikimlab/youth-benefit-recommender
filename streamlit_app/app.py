import sys
import os
import streamlit as st
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.recommender import recommend

# Load policy data
df = pd.read_csv("data/sample.csv")

st.set_page_config(page_title="청년 정책 추천기", layout="centered")
st.title("🎯 청년 정책 추천 시스템")

# --- 사용자 입력 폼 ---
st.subheader("🧍 나의 정보 입력")

age = st.number_input("나이", min_value=18, max_value=39, value=29)
income = st.number_input("월 소득 (만원)", min_value=0, value=230)
region = st.selectbox("거주 지역", ["서울", "경기도", "부산", "대구", "전국"])
job_status = st.selectbox("고용 상태", ["무직", "재직"])
household_type = st.selectbox("가구 형태", ["독립가구", "무관", "부모동거"])

user_input = {
    "age": age,
    "income": income,
    "region": region,
    "job_status": job_status,
    "household_type": household_type
}

if st.button("📌 추천 정책 보기"):
    st.subheader("✅ 추천 결과")
    results = recommend(user_input, df)

    if results.empty or results["recommendation_score"].max() == 0:
        st.warning("해당 조건에 맞는 정책이 없어요 😢")
    else:
        for _, row in results.iterrows():
            st.markdown(f"### {row['policy_name']} (점수: {row['recommendation_score']})")
            st.write(row['reason'])
            st.markdown(f"[정책 상세 보기]({row['policy_url']})")
            st.markdown("---")
