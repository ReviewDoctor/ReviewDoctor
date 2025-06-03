import streamlit as st
import pandas as pd
from src.report_generator import generate_reports
import tempfile
import os

st.title("리뷰 기반 자동 리포트 생성기")

uploaded_file = st.file_uploader("CSV 리뷰 파일 업로드", type=["csv"])

if uploaded_file:
    # 임시 저장소에 파일 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if st.button("리포트 생성"):
        with st.spinner("GPT로 리포트 생성 중..."):
            try:
                marketing_report, service_report = generate_reports(tmp_path)

                st.success("리포트 생성 완료!")

                st.subheader("마케팅 전략 리포트")
                st.text_area("Marketing Report", marketing_report, height=400)

                st.download_button("⬇마케팅 리포트 다운로드", marketing_report, file_name="marketing_report.txt")

                st.subheader("서비스 개선 전략 리포트")
                st.text_area("Service Report", service_report, height=400)

                st.download_button("⬇서비스 리포트 다운로드", service_report, file_name="service_report.txt")

            except Exception as e:
                st.error(f"에러 발생: {e}")
    else:
        st.info("버튼을 눌러 리포트를 생성하세요.")
else:
    st.warning("먼저 CSV 파일을 업로드해주세요.")
