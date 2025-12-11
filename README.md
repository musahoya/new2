# ✨ 프롬프트 엔지니어링 자동화

AI를 활용하여 최적화된 프롬프트를 자동으로 생성하는 웹 애플리케이션입니다.

## 🎯 주요 기능

### 워크플로우

```
[1단계] 사용자 입력
    ↓
[2단계] AI가 웹 검색 (10가지 트렌드/정보 수집)
    ↓
[3단계] 의도 파악 및 정리
    ↓
[4단계] 사용자 확인
    ↓
[5단계] 5가지 전략별 프롬프트 생성
    - CoT (논리적 단계)
    - Few-Shot (예시 기반)
    - Meta-Prompting (전문가 페르소나)
    - Self-Refine (반복 개선)
    - Structured Context (구조화 분석)
    ↓
[6단계] 사용자 선택 → 최적 프롬프트 제공
```

### 5가지 프롬프팅 전략

1. **🧠 CoT (Chain of Thought)** - 사고 연쇄
   - 논리적 단계별 사고 과정
   - 복잡한 계획, 분석, 문제 해결에 최적

2. **📝 Few-Shot Learning** - 예시 학습
   - 구체적인 예시를 통한 스타일 모방
   - 블로그, 에세이, 스타일 통일이 필요한 콘텐츠에 최적

3. **👨‍🏫 Meta-Prompting** - 전문가 페르소나
   - 전문가 역할을 부여한 심층 분석
   - 객관적 리뷰, 분석, 권위 있는 콘텐츠에 최적

4. **🔄 Self-Refine** - 자체 개선
   - 초안부터 시작해 반복적으로 개선
   - 고퀄리티 콘텐츠, 정교한 글쓰기에 최적

5. **📊 Structured Context** - 구조화 분석
   - 체계적인 보고서 형식의 심층 분석
   - 데이터 분석, 리서치 보고서에 최적

## 🏗️ 프로젝트 구조

```
prompt-engineering-automation/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── models/            # 데이터 모델
│   │   │   └── schemas.py
│   │   ├── services/          # 핵심 비즈니스 로직
│   │   │   ├── intent_analyzer.py      # 의도 파악 엔진
│   │   │   ├── trend_collector.py      # 트렌드 수집 엔진
│   │   │   ├── prompt_generator.py     # 프롬프트 생성 엔진
│   │   │   └── confirmation_module.py  # 사용자 확인 모듈
│   │   ├── config.py          # 설정 관리
│   │   └── main.py            # FastAPI 앱
│   ├── requirements.txt
│   └── .env.example
├── frontend/                   # Streamlit 프론트엔드
│   ├── app.py
│   └── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd prompt-engineering-automation
```

### 2. 백엔드 설정

```bash
cd backend

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY를 입력하세요
```

### 3. 환경 변수 설정

`.env` 파일에 다음을 설정하세요:

```bash
# 필수: Anthropic API Key
ANTHROPIC_API_KEY=your_api_key_here

# 선택: 웹 검색 API (현재는 시뮬레이션 데이터 사용)
# BRAVE_SEARCH_API_KEY=your_brave_api_key_here
# GOOGLE_SEARCH_API_KEY=your_google_api_key_here
# GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
```

### 4. 백엔드 서버 실행

```bash
cd backend
python -m uvicorn app.main:app --reload
```

백엔드 서버가 `http://localhost:8000`에서 실행됩니다.

### 5. 프론트엔드 실행

새 터미널을 열고:

```bash
cd frontend

# 의존성 설치
pip install -r requirements.txt

# Streamlit 앱 실행
streamlit run app.py
```

프론트엔드가 자동으로 브라우저에서 열립니다 (보통 `http://localhost:8501`).

## 📖 사용 방법

### 웹 인터페이스 (Streamlit)

1. 브라우저에서 `http://localhost:8501` 접속
2. 원하는 내용을 입력 (예: "제주도 3박4일 여행 계획")
3. AI가 자동으로 분석 및 트렌드 수집
4. 분석 결과 확인
5. 5가지 프롬프팅 전략 중 선택
6. 생성된 프롬프트를 복사하여 사용

### API 사용

#### 전체 파이프라인

```bash
curl -X POST "http://localhost:8000/api/pipeline" \
  -H "Content-Type: application/json" \
  -d '{"query": "제주도 3박4일 여행 계획"}'
```

#### 단계별 실행

**1단계: 분석**

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "제주도 3박4일 여행 계획"}'
```

**2단계: 프롬프트 생성**

```bash
curl -X POST "http://localhost:8000/api/generate-prompts" \
  -H "Content-Type: application/json" \
  -d '{분석결과}'
```

#### 사용 가능한 전략 조회

```bash
curl http://localhost:8000/api/strategies
```

## 🎨 사용 예시

### 예시 1: 여행 블로그

**입력:**
```
겨울 서울 데이트 코스 추천 글 써야 해
```

**결과:**
- AI가 "서울 겨울 데이트" 트렌드 수집
- 성수동 팝업스토어, 한강 야경 카페 등 최신 정보 반영
- 5가지 스타일의 프롬프트 생성
- Few-Shot 선택 시 → 감성적인 블로그 스타일 프롬프트 제공

### 예시 2: 투자 분석

**입력:**
```
2025년 반도체 산업 투자 전망 정리
```

**결과:**
- AI가 반도체 시장, AI칩 수요 등 최신 트렌드 수집
- Structured 전략 추천
- 체계적인 보고서 형식의 프롬프트 제공

## 🔧 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 프레임워크
- **Anthropic Claude API**: AI 엔진
- **Pydantic**: 데이터 검증
- **HTTPX**: 비동기 HTTP 클라이언트

### 프론트엔드
- **Streamlit**: 인터랙티브 웹 UI
- **Requests**: HTTP 클라이언트

## 🌟 핵심 모듈

### IntentAnalyzer (의도 파악 엔진)
- 사용자 쿼리를 분석하여 의도 파악
- 키워드 추출, 대상 독자 식별
- 적절한 출력 형식 결정

### TrendCollector (트렌드 수집 엔진)
- 웹 검색을 통한 최신 정보 수집
- 10가지 핵심 트렌드 정리
- 전체 요약 생성

### PromptGenerator (프롬프트 생성 엔진)
- 5가지 프롬프팅 전략 구현
- 트렌드와 의도를 반영한 프롬프트 생성
- 각 전략에 최적화된 구조 제공

### ConfirmationModule (사용자 확인 모듈)
- 분석 결과 확인 메시지 생성
- 전략 선택 가이드 제공

## 🔐 보안 및 설정

### API 키 관리
- `.env` 파일에 API 키 저장 (`.gitignore`에 포함됨)
- 환경 변수를 통한 안전한 관리

### CORS 설정
- 프로덕션 환경에서는 `main.py`의 CORS 설정을 특정 도메인만 허용하도록 변경하세요

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 특정 도메인만
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📈 확장 가능성

### 현재 시뮬레이션 → 실제 웹 검색
- `trend_collector.py`에서 Brave Search API 또는 Google Custom Search API 연동
- 주석 처리된 코드 참고

### 데이터베이스 추가
- PostgreSQL로 사용자 히스토리 저장
- Vector DB로 프롬프트 템플릿 관리

### 고급 기능
- 사용자 선호도 학습
- 프롬프트 버전 관리
- 팀 협업 기능
- 커스텀 전략 추가

## 💡 팁

### 더 나은 결과를 위해
1. **구체적으로 입력하세요**
   - ❌ "여행 계획"
   - ✅ "제주도 3박4일 가족 여행 계획, 자연 중심"

2. **형식을 명시하세요**
   - "블로그 글로", "분석 보고서로", "가이드로"

3. **대상을 언급하세요**
   - "20-30대 커플을 위한", "초보 투자자를 위한"

## 🐛 문제 해결

### 백엔드 서버 연결 실패
```
⚠️ 백엔드 서버에 연결할 수 없습니다.
```
- 백엔드 서버가 실행 중인지 확인하세요
- `cd backend && python -m uvicorn app.main:app --reload`

### API 키 오류
```
❌ API 호출 실패: 401 Unauthorized
```
- `.env` 파일에 올바른 `ANTHROPIC_API_KEY`가 설정되어 있는지 확인하세요

### 모듈 import 오류
```
ModuleNotFoundError: No module named 'anthropic'
```
- 의존성을 설치했는지 확인하세요: `pip install -r requirements.txt`

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🤝 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

## 📧 문의

질문이나 제안이 있으시면 이슈를 열어주세요.

---

**Made with ❤️ and AI**
