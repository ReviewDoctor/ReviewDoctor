import streamlit as st

st.set_page_config(page_title="Review Report Generator", page_icon="🛫")

st.title("리뷰 기반 리포트 생성기")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 리뷰 파일 업로드", type=["csv"])

if uploaded_file:
    st.session_state["uploaded_file"] = uploaded_file
    st.success("파일 업로드 완료! 왼쪽 메뉴로 이동하세요.")
else:
    st.info("먼저 리뷰 CSV 파일을 업로드해주세요.")

# st.markdown("""
# ---  
# 왼쪽 사이드바에서 기능을 선택하세요:
# - 리뷰 분석
# - GPT 리포트 생성
# """)
