# import streamlit as st
# import plotly.graph_objects as go

# # ----------------------------
# # ✅ 샘플 데이터
# # ----------------------------
# # {연도: {월: {좌석 등급: {'good': [...], 'bad': [...]}}}}
# sample_review_data = {
#     2025: {
#         5: {
#             "이코노미": {
#                 "good": [("좌석", 0.1), ("서비스", 0.06), ("식음료", 0.03)],
#                 "bad": [("지상 서비스", 0.05), ("식음료", 0.04), ("엔터테인먼트", 0.03)]
#             },
#             "비즈니스": {
#                 "good": [("식사", 0.15), ("좌석", 0.13), ("서비스", 0.12)],
#                 "bad": [("엔터테인먼트", 0.04)]
#             }
#         },
#         4: {
#             "이코노미": {
#                 "good": [("좌석", 0.09), ("서비스", 0.05), ("식음료", 0.03)],
#                 "bad": [("지상 서비스", 0.06), ("식음료", 0.04), ("엔터테인먼트", 0.02)]
#             },
#             "비즈니스": {
#                 "good": [("식사", 0.14), ("좌석", 0.12), ("서비스", 0.1)],
#                 "bad": [("엔터테인먼트", 0.05)]
#             }
#         }
#     },
#     2024: {
#         5: {
#             "이코노미": {
#                 "good": [("좌석", 0.09), ("서비스", 0.05), ("식음료", 0.03)],
#                 "bad": [("지상 서비스", 0.06), ("식음료", 0.04), ("엔터테인먼트", 0.02)]
#             },
#             "비즈니스": {
#                 "good": [("식사", 0.14), ("좌석", 0.12), ("서비스", 0.1)],
#                 "bad": [("엔터테인먼트", 0.05)]
#             }
#         }
#     }
# }

# strengths = {
#     "이코노미": "편한 좌석, 객실 승무원 서비스",
#     "프리미엄 이코노미": "넓은 좌석, 빠른 체크인",
#     "비즈니스": "최상급 좌석, 프리미엄 식사, 객실 승무원 서비스",
#     "퍼스트": "프라이빗 좌석, 전용 라운지, 고급 식음료"
# }
# weaknesses = {
#     "이코노미": "지상 서비스, 기내 식음료, 기내 엔터테인먼트",
#     "프리미엄 이코노미": "지상 서비스, 기내 와이파이",
#     "비즈니스": "엔터테인먼트 다양성",
#     "퍼스트": "가격 대비 가치"
# }

# # ----------------------------
# # ✅ UI 요소
# # ----------------------------
# st.title("항공사 리뷰 분석")

# # 좌석 등급
# seat_class = st.radio(
#     "좌석 등급을 선택하세요:",
#     ["이코노미", "프리미엄 이코노미", "비즈니스", "퍼스트"],
#     horizontal=True
# )

# # 연도 & 월 선택
# col1, col2 = st.columns(2)
# with col1:
#     years = sorted(sample_review_data.keys())
#     selected_year = st.selectbox("연도 선택", years)
# with col2:
#     months = sorted(sample_review_data[selected_year].keys())
#     selected_month = st.selectbox("월 선택", months)




# # ----------------------------
# # ✅ 데이터 로드
# # ----------------------------
# review_data = sample_review_data.get(selected_year, {}).get(selected_month, {}).get(seat_class)

# # ----------------------------
# # ✅ 데이터 없는 경우 처리
# # ----------------------------
# if review_data is None:
#     st.warning("해당 기간의 데이터가 없습니다.")
# else:
#     # 문구 출력
#     st.markdown(f"""
#     ### {selected_year}년 {selected_month}월 {seat_class} 리뷰 요약  
#     :green[**{strengths.get(seat_class, '-')}**] 가 강점이고,  
#     :red[**{weaknesses.get(seat_class, '-')}**] 의 보완이 필요해요.
#     """)

#     # 그래프 출력
#     st.subheader("항공사 리뷰 통계 (긍정/부정)")
#     good_labels = [label for label, _ in review_data["good"]]
#     good_vals = [val for _, val in review_data["good"]]
#     bad_labels = [label for label, _ in review_data["bad"]]
#     bad_vals = [val for _, val in review_data["bad"]]

#     all_labels = sorted(set(good_labels + bad_labels))
#     values_good = [dict(review_data["good"]).get(label, 0) for label in all_labels]
#     values_bad = [dict(review_data["bad"]).get(label, 0) for label in all_labels]

#     fig = go.Figure(data=[
#         go.Bar(name="긍정", x=all_labels, y=values_good, marker_color='lightblue'),
#         go.Bar(name="부정", x=all_labels, y=values_bad, marker_color='salmon')
#     ])
#     fig.update_layout(barmode='group', height=400)
#     st.plotly_chart(fig)

#     # 항목별 퍼센트
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("#### 좋았어요")
#         for label, ratio in review_data["good"]:
#             st.progress(ratio, text=f"{label} {round(ratio*100,1)}%")
#     with col2:
#         st.markdown("#### 아쉬웠어요")
#         for label, ratio in review_data["bad"]:
#             st.progress(ratio, text=f"{label} {round(ratio*100,1)}%")