import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="리뷰 분석", page_icon="📊")
st.title(":blue[항공사 좌석별 리뷰 데이터 분석]")

# 세션에서 파일 불러오기
if "uploaded_file" not in st.session_state:
    st.warning("메인 페이지에서 CSV 파일을 먼저 업로드해주세요.")
    st.stop()

uploaded_file = st.session_state["uploaded_file"]
uploaded_file.seek(0)
df = pd.read_csv(uploaded_file)

# CSV 업로드 미리보기
# st.subheader("업로드된 리뷰 데이터 미리보기")
# st.dataframe(df.head(10))

# 1. 데이터 전처리 함수
def preprocess_data(df):
    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()
    
    # SeatType 열의 내용을 한글로 변경
    seat_type_mapping = {
        'Business Class': '비즈니스',
        'Economy Class': '이코노미',
        'First Class': '퍼스트',
        'Premium Economy': '프리미엄 이코노미'
    }
    df['SeatType'] = df['SeatType'].map(seat_type_mapping).fillna(df['SeatType'])
    
    # 날짜 생성: 홀수 행은 2025년 5월, 짝수 행은 2025년 6월
    df['year'] = 2025
    df['month'] = df.index.map(lambda x: 5 if x % 2 == 0 else 6)
    
    # Recommended를 good/bad로 매핑
    df['sentiment'] = df['Recommended'].map({'yes': 'good', 'no': 'bad'})
    
    # 명사(Nouns) 전처리
    df['Nouns'] = df['Nouns'].fillna('').apply(lambda x: [word.strip() for word in str(x).split(',')])
    
    return df

# 2. 리뷰 데이터 생성 함수
def build_review_data(df):
    review_data = {}
    
    for (year, month, seat_class), group in df.groupby(['year', 'month', 'SeatType']):
        if year not in review_data:
            review_data[year] = {}
        if month not in review_data[year]:
            review_data[year][month] = {}
        
        good_data = group[group['sentiment'] == 'good']
        bad_data = group[group['sentiment'] == 'bad']
        
        # 여행객 유형 분포
        traveller_dist = group['TypeOfTraveller'].value_counts(normalize=True).to_dict()
        
        # 감성 분포
        sentiment_dist = group['sentiment'].value_counts(normalize=True).to_dict()
        
        review_data[year][month][seat_class] = {
            "traveller_dist": traveller_dist,
            "sentiment_dist": sentiment_dist
        }
    
    return review_data

# 3. 강점/약점 분석 함수
def build_strengths_weaknesses(df):
    strengths = {}
    weaknesses = {}
    
    for seat_class in df['SeatType'].unique():
        # 긍정 리뷰 명사 추출
        good_nouns = []
        for nouns in df[(df['SeatType'] == seat_class) & (df['sentiment'] == 'good')]['Nouns']:
            good_nouns.extend(nouns)
        
        # 부정 리뷰 명사 추출
        bad_nouns = []
        for nouns in df[(df['SeatType'] == seat_class) & (df['sentiment'] == 'bad')]['Nouns']:
            bad_nouns.extend(nouns)
        
        # 상위 5개 명사 추출 (빈도순)
        top_good = [word for word, _ in Counter(good_nouns).most_common(5)] if good_nouns else ["데이터 없음"]
        top_bad = [word for word, _ in Counter(bad_nouns).most_common(5)] if bad_nouns else ["데이터 없음"]
        
        strengths[seat_class] = ", ".join(top_good)
        weaknesses[seat_class] = ", ".join(top_bad)
    
    return strengths, weaknesses

# 4. 평점 데이터 생성 함수
def build_rating_data(df):
    rating_data = {}
    # 서비스 항목 컬럼
    service_columns = ['SeatComfort', 'CabinStaffService', 'Food&Beverages', 'GroundService', 'InflightEntertainment']
    
    for (year, month, seat_class), group in df.groupby(['year', 'month', 'SeatType']):
        if year not in rating_data:
            rating_data[year] = {}
        if month not in rating_data[year]:
            rating_data[year][month] = {}
        
        # 서비스 항목별 평균 평점 계산
        avg_ratings = {}
        for col in service_columns:
            if col in group.columns:
                avg_ratings[col] = group[col].mean()
            else:
                avg_ratings[col] = 0.0  # 컬럼이 없는 경우 기본값
        
        # 전체 평점
        avg_ratings['OverallRating'] = group['OverallRating'].mean()
        
        rating_data[year][month][seat_class] = avg_ratings
    
    return rating_data

# 5. 여행객 유형 데이터 생성
def build_traveller_data(df):
    traveller_data = {}
    
    for (year, month), group in df.groupby(['year', 'month']):
        if year not in traveller_data:
            traveller_data[year] = {}
        if month not in traveller_data[year]:
            traveller_data[year][month] = {}
        
        # 좌석 타입별 여행객 유형 분포
        for seat_class in group['SeatType'].unique():
            class_group = group[group['SeatType'] == seat_class]
            dist = class_group['TypeOfTraveller'].value_counts(normalize=True).to_dict()
            traveller_data[year][month][seat_class] = dist
    
    return traveller_data

# 6. 데이터 전처리 및 분석
try:
    # 데이터 전처리
    processed_df = preprocess_data(df)
    
    # 분석 데이터 생성
    review_data = build_review_data(processed_df)
    strengths, weaknesses = build_strengths_weaknesses(processed_df)
    rating_data = build_rating_data(processed_df)
    traveller_data = build_traveller_data(processed_df)
    
    # 디버깅 정보 출력
    # st.success("리뷰 분석 완료!")
    
except Exception as e:
    st.error(f"리뷰 csv 분석 중 오류 발생: {str(e)}")
    st.write("데이터프레임 컬럼 목록:", df.columns.tolist())
    st.stop()

# --- UI 및 시각화  -------------------------------------
# st.title("리뷰 데이터 분석")

# 좌석 종류 선택
# seat_classes = processed_df['SeatType'].unique().tolist()
# seat_class = st.radio("**좌석 종류를 골라주세요.**", seat_classes, horizontal=True)
# 좌석 종류 선택
seat_classes = processed_df['SeatType'].unique().tolist()

# 좌석 종류를 버튼 스타일로 표시
st.markdown("**좌석 종류를 골라주세요.**")
cols = st.columns(len(seat_classes))
if 'selected_seat_class' not in st.session_state:
    st.session_state.selected_seat_class = seat_classes[0]

for i, seat_type in enumerate(seat_classes):
    with cols[i]:
        if st.button(
            seat_type, 
            key=f"seat_{seat_type}",
            use_container_width=True,
            type="secondary" if st.session_state.selected_seat_class == seat_type else "secondary"
        ):
            st.session_state.selected_seat_class = seat_type

seat_class = st.session_state.selected_seat_class

# 연도 및 월 선택
col1, col2 = st.columns(2)
with col1:
    available_years = list(review_data.keys())
    selected_year = st.selectbox("**연도를 선택해주세요.**", available_years)
with col2:
    if selected_year in review_data:
        available_months = list(review_data[selected_year].keys())
        selected_month = st.selectbox("**월을 선택해주세요.**", available_months)
    else:
        st.warning("선택한 연도에 데이터가 없습니다.")
        st.stop()

# 선택한 데이터 가져오기
current_review = review_data[selected_year][selected_month].get(seat_class)
current_rating = rating_data[selected_year][selected_month].get(seat_class)
current_traveller = traveller_data[selected_year][selected_month].get(seat_class)

# 데이터가 없는 경우 에러 처리
if not current_review or not current_rating or not current_traveller:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    st.stop()

# 1. 리뷰 요약 섹션 -----------------------------------
st.markdown(f""" --- """)
st.markdown(f""" ## :blue[{selected_year}년 {selected_month}월 {seat_class}의 리뷰 요약] """)

# 감성 분포 파이 차트
st.subheader("감성 분포")
sentiment_labels = list(current_review['sentiment_dist'].keys())
sentiment_values = list(current_review['sentiment_dist'].values())

fig_sentiment = go.Figure(data=[go.Pie(
    labels=sentiment_labels,
    values=sentiment_values,
    hole=0.3,
    marker_colors=['lightgreen', 'lightcoral']
)])
st.plotly_chart(fig_sentiment)

# 강점/약점 표시
st.success(f"**우리 항공사의 마케팅 포인트:** {strengths[seat_class]}")
st.error(f"**우리 항공사의 개선 사항:** {weaknesses[seat_class]}")

# 2. 여행객 유형 분석 -----------------------------------
st.markdown("---")
st.subheader("여행객 유형 분포")

# 여행객 유형 파이 차트
traveller_labels = list(current_traveller.keys())
traveller_values = list(current_traveller.values())

fig_traveller = go.Figure(data=[go.Pie(
    labels=traveller_labels,
    values=traveller_values,
    hole=0.3
)])
st.plotly_chart(fig_traveller)

# 3. 서비스 평점 레이더 차트 -----------------------------------
st.markdown("---")
st.subheader("서비스 항목별 평점 분석")

# 레이더 차트 데이터 준비
service_categories = ['SeatComfort', 'CabinStaffService', 'Food&Beverages', 'GroundService', 'InflightEntertainment']
current_ratings = [current_rating[cat] for cat in service_categories]

# 이전 달 데이터 가져오기
prev_month = selected_month - 1
prev_ratings = None

if prev_month > 0 and selected_year in rating_data and prev_month in rating_data[selected_year]:
    prev_rating_data = rating_data[selected_year][prev_month].get(seat_class)
    if prev_rating_data:
        prev_ratings = [prev_rating_data[cat] for cat in service_categories]

# 레이더 차트 생성
fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=current_ratings,
    theta=service_categories,
    fill='toself',
    name=f'{selected_month}월',
    line_color='blue'
))

if prev_ratings:
    fig_radar.add_trace(go.Scatterpolar(
        r=prev_ratings,
        theta=service_categories,
        fill='toself',
        name=f'{prev_month}월',
        line_color='red'
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        )),
    showlegend=True,
    title=f"{seat_class} 서비스 항목별 평점 비교",
    height=500
)

st.plotly_chart(fig_radar)

# 4. 전월 대비 평점 변화 분석 -----------------------------------
st.markdown("---")
st.subheader("전월 대비 평점 변화 분석")

if prev_ratings:
    # 평점 변화 계산
    rating_changes = [current - prev for current, prev in zip(current_ratings, prev_ratings)]
    
    # 변화 시각화
    fig_change = go.Figure()
    fig_change.add_trace(go.Bar(
        x=service_categories,
        y=rating_changes,
        marker_color=np.where(np.array(rating_changes) >= 0, 'green', 'red'),
        text=[f"{change:.2f}" for change in rating_changes],
        textposition='auto'
    ))
    
    fig_change.update_layout(
        title=f"{prev_month}월 대비 {selected_month}월 평점 변화",
        yaxis_title="평점 변화",
        height=400
    )
    
    st.plotly_chart(fig_change)
    
    # 개선 여부 분석
    improvements = [cat for cat, change in zip(service_categories, rating_changes) if change > 0]
    declines = [cat for cat, change in zip(service_categories, rating_changes) if change < 0]
    
    if improvements:
        st.success(f"**개선된 서비스:** {', '.join(improvements)}")
    if declines:
        st.error(f"**악화된 서비스:** {', '.join(declines)}")
else:
    st.info("이전 달 데이터가 없어 비교 분석을 수행할 수 없습니다.")

# 5. 명사 워드클라우드 및 막대그래프 -----------------------------------
st.markdown("---")
st.subheader("리뷰 키워드 분석")

# 시각화 방식 선택 버튼
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    show_wordcloud = st.button("워드 클라우드로 보기", type="secondary")
with col_btn2:
    show_chart = st.button("그래프로 보기", type="secondary")

# 세션 상태 초기화
if 'visualization_mode' not in st.session_state:
    st.session_state.visualization_mode = 'wordcloud'

# 버튼 클릭에 따른 모드 변경
if show_wordcloud:
    st.session_state.visualization_mode = 'wordcloud'
elif show_chart:
    st.session_state.visualization_mode = 'chart'

# 긍정/부정 리뷰 데이터 추출
good_df = processed_df[(processed_df['SeatType'] == seat_class) & 
                      (processed_df['sentiment'] == 'good') &
                      (processed_df['year'] == selected_year) &
                      (processed_df['month'] == selected_month)]

bad_df = processed_df[(processed_df['SeatType'] == seat_class) & 
                     (processed_df['sentiment'] == 'bad') &
                     (processed_df['year'] == selected_year) &
                     (processed_df['month'] == selected_month)]

# 긍정 리뷰 명사 추출 및 빈도 계산
good_nouns = []
for nouns in good_df['Nouns']:
    good_nouns.extend(nouns)
good_counter = Counter(good_nouns)

# 부정 리뷰 명사 추출 및 빈도 계산
bad_nouns = []
for nouns in bad_df['Nouns']:
    bad_nouns.extend(nouns)
bad_counter = Counter(bad_nouns)

col1, col2 = st.columns(2)

if st.session_state.visualization_mode == 'wordcloud':
    # 워드클라우드 표시
    with col1:
        st.markdown("#### :green[좋았어요]")
        if good_nouns:
            text = ' '.join(good_nouns)
            # 긍정 리뷰용 green 계열 색상 함수
            def green_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                return f"hsl({np.random.randint(90, 150)}, {np.random.randint(70, 100)}%, {np.random.randint(30, 70)}%)"
            
            wordcloud = WordCloud(
                width=400, 
                height=300, 
                background_color='white',
                color_func=green_color_func
            ).generate(text)
            plt.figure(figsize=(10, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        else:
            st.info("긍정 리뷰 데이터가 없습니다.")

    with col2:
        st.markdown("#### :red[아쉬웠어요]")
        if bad_nouns:
            text = ' '.join(bad_nouns)
            # 부정 리뷰용 red 계열 색상 함수
            def red_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                return f"hsl({np.random.randint(0, 30)}, {np.random.randint(70, 100)}%, {np.random.randint(30, 70)}%)"
            
            wordcloud = WordCloud(
                width=400, 
                height=300, 
                background_color='white',
                color_func=red_color_func
            ).generate(text)
            plt.figure(figsize=(10, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        else:
            st.info("부정 리뷰 데이터가 없습니다.")

else:
    # 막대그래프 표시
    with col1:
        # st.markdown("#### :green[좋았어요]")
        if good_counter:
            # 상위 10개 키워드
            top_good = good_counter.most_common(10)
            words, counts = zip(*top_good)
            
            fig_good = go.Figure(go.Bar(
                x=list(counts),
                y=list(words),
                orientation='h',
                marker_color='green',
                text=list(counts),
                textposition='auto'
            ))
            fig_good.update_layout(
                title="긍정 키워드 빈도",
                xaxis_title="빈도",
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_good, use_container_width=True)
        else:
            st.info("긍정 리뷰 데이터가 없습니다.")

    with col2:
        # st.markdown("#### :red[아쉬웠어요]")
        if bad_counter:
            # 상위 10개 키워드
            top_bad = bad_counter.most_common(10)
            words, counts = zip(*top_bad)
            
            fig_bad = go.Figure(go.Bar(
                x=list(counts),
                y=list(words),
                orientation='h',
                marker_color='red',
                text=list(counts),
                textposition='auto'
            ))
            fig_bad.update_layout(
                title="부정 키워드 빈도",
                xaxis_title="빈도",
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_bad, use_container_width=True)
        else:
            st.info("부정 리뷰 데이터가 없습니다.")

# 6. 리포트 생성 페이지로 이동 버튼
st.markdown("---")
if st.button("리포트 생성하러 가기"):
    st.switch_page("pages/2_generate_report.py")