# ReviewDoctor
리뷰닥터 레포지토리입니다.

## Streamlit 
- stream 설치하기
  `pip install streamlit`

- steramlit이 잘 설치되었는지 확인
  `streamlit hello`

- streamlit로 파이썬 실행하기
  `streamlit run (파일명).py`

---

## Azure OpenAI 디렉토리 구조

ReviewDoctor/
├── data/ # 리뷰 CSV 파일
│ └── adjectives_with_service_ratings.csv
├── src/
│ ├── gpt_client.py # Azure OpenAI 호출
│ └── report_generator.py # 리뷰 분리 + 프롬프트 생성 + 응답 처리
├── streamlit_app.py # Streamlit 앱
├── main.py # CLI 실행용 진입점
├── .env # (로컬 전용) Azure API 키
├── .env.example # 공유용 환경 변수 템플릿
├── requirements.txt # 설치 패키지 목록
└── README.md

---

## .env 설정

루트 디렉토리에 `.env` 파일을 생성하고 다음 정보를 입력하세요:

```env
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://smu-3team.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=smu-3team-gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-01-01-preview

---

## 실행 방법

1. 의존성 설치
`pip install -r requirements.txt`

2. Streamlit 앱 실행
`python -m streamlit run streamlit_app.py`