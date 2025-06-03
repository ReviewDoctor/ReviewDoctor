import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="리뷰 분석", page_icon="📊")
st.title("업로드한 리뷰 데이터 분석")

# 세션에서 파일 불러오기
if "uploaded_file" not in st.session_state:
    st.warning("메인 페이지에서 CSV 파일을 먼저 업로드해주세요.")
    st.stop()

uploaded_file = st.session_state["uploaded_file"]
uploaded_file.seek(0)

df = pd.read_csv(uploaded_file)

# CSV 업로드 미리보기
st.subheader("업로드된 리뷰 데이터 미리보기")
st.dataframe(df.head(10))

# --- 더미 데이터 (분석 코드 넣기) ---
sample_review_data = {
    2025: {
        5: {
            "Economy": {
                "good": [("Seats", 0.1), ("Service", 0.06), ("Food", 0.03)],
                "bad": [("Ground Service", 0.05), ("Food", 0.04), ("Entertainment", 0.03)]
            },
            "Premium Economy": {
                "good": [("Seats", 0.1), ("Service", 0.06), ("Food", 0.03)],
                "bad": [("Ground Service", 0.05), ("Food", 0.04), ("Entertainment", 0.03)]
            },
            
            "Business": {
                "good": [("Meal", 0.15), ("Seats", 0.13), ("Service", 0.12)],
                "bad": [("Entertainment", 0.04)]
            },
            "First Class": {
                "good": [("Meal", 0.15), ("Seats", 0.13), ("Service", 0.12)],
                "bad": [("Entertainment", 0.04)]
            }
        }
    }
}

strengths = {
    "Economy": "Comfortable seats, friendly cabin staff",
    "Premium Economy": "good(CabinStaffService)",
    "Business": "Premium seats, excellent meals, attentive service",
    "First Class": "friendly(CabinStaffService), comfortable(SeatComfort)",
}
weaknesses = {
    "Economy": "Ground service, in-flight food, entertainment",
    "Premium Economy": "slow(Food&Beverages), awful(Food&Beverages)",
    "Business": "Limited entertainment variety, available(SeatComfort)",
    "First Class": "poor(InflightEntertainment), slow(Food&Beverages)"
}

# --- UI ---
st.title("리뷰 데이터 분석 (샘플)")

seat_class = st.radio("좌석 종류를 골라주세요.", list(strengths.keys()), horizontal=True)

col1, col2 = st.columns(2)
with col1:
    selected_year = st.selectbox("연도를 선택해주세요.", list(sample_review_data.keys()))
with col2:
    selected_month = st.selectbox("월을 선택해주세요.", list(sample_review_data[selected_year].keys()))

review_data = sample_review_data[selected_year][selected_month].get(seat_class)

if review_data is None:
    st.warning("No data available.")
else:
    st.markdown(f""" --- """)
    st.markdown(f""" ## :blue[{selected_year}년 {selected_month}월 {seat_class}의 리뷰 요약] """)

    st.subheader("항공사 리뷰 통계")
    all_labels = sorted(set([l for l, _ in review_data["good"] + review_data["bad"]]))
    good_values = [dict(review_data["good"]).get(l, 0) for l in all_labels]
    bad_values = [dict(review_data["bad"]).get(l, 0) for l in all_labels]

    fig = go.Figure(data=[
        go.Bar(name="긍정", x=all_labels, y=good_values, marker_color='lightgreen'),
        go.Bar(name="부정", x=all_labels, y=bad_values, marker_color='lightcoral')
    ])
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 좋았어요")
        for label, ratio in review_data["good"]:
            st.progress(ratio, text=f"{label} {round(ratio*100, 1)}%")
    with col2:
        st.markdown("#### 아쉬웠어요")
        for label, ratio in review_data["bad"]:
            st.progress(ratio, text=f"{label} {round(ratio*100, 1)}%")

    st.markdown(f"""
 
    **- 우리 항공사의 마케팅 포인트:** :green[**{strengths[seat_class]}**]  
    **- 우리 항공사의 개선 사항:** :red[**{weaknesses[seat_class]}**]
    
    """)

    # 리포트 생성 페이지로 이동 버튼
    st.markdown("---")
    if st.button("리포트 생성하러 가기"):
        st.switch_page("pages/2_generate_report.py")
