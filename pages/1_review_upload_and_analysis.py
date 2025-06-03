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
            "Business": {
                "good": [("Meal", 0.15), ("Seats", 0.13), ("Service", 0.12)],
                "bad": [("Entertainment", 0.04)]
            }
        }
    }
}

strengths = {
    "Economy": "Comfortable seats, friendly cabin staff",
    "Business": "Premium seats, excellent meals, attentive service"
}
weaknesses = {
    "Economy": "Ground service, in-flight food, entertainment",
    "Business": "Limited entertainment variety"
}

# --- UI ---
st.title("리뷰 데이터 분석 (샘플)")

seat_class = st.radio("Choose seat class:", list(strengths.keys()), horizontal=True)

col1, col2 = st.columns(2)
with col1:
    selected_year = st.selectbox("Select year", list(sample_review_data.keys()))
with col2:
    selected_month = st.selectbox("Select month", list(sample_review_data[selected_year].keys()))

review_data = sample_review_data[selected_year][selected_month].get(seat_class)

if review_data is None:
    st.warning("No data available.")
else:
    st.markdown(f"""
    ### {selected_year}-{selected_month} {seat_class} 리뷰 요약  
    Strengths: :green[**{strengths[seat_class]}**]  
    Weaknesses: :red[**{weaknesses[seat_class]}**]
    """)

    st.subheader("Sentiment Distribution")
    all_labels = sorted(set([l for l, _ in review_data["good"] + review_data["bad"]]))
    good_values = [dict(review_data["good"]).get(l, 0) for l in all_labels]
    bad_values = [dict(review_data["bad"]).get(l, 0) for l in all_labels]

    fig = go.Figure(data=[
        go.Bar(name="Positive", x=all_labels, y=good_values, marker_color='lightgreen'),
        go.Bar(name="Negative", x=all_labels, y=bad_values, marker_color='lightcoral')
    ])
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Positive")
        for label, ratio in review_data["good"]:
            st.progress(ratio, text=f"{label} {round(ratio*100, 1)}%")
    with col2:
        st.markdown("#### Negative")
        for label, ratio in review_data["bad"]:
            st.progress(ratio, text=f"{label} {round(ratio*100, 1)}%")

    # 리포트 생성 페이지로 이동 버튼
    st.markdown("---")
    if st.button("리포트 생성하러 가기"):
        st.switch_page("pages/2_generate_report.py")
