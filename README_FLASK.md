# ✨ 프롬프트 엔지니어링 자동화 (Flask 버전)

AI를 활용하여 최적화된 프롬프트를 자동으로 생성하는 웹 애플리케이션입니다.

> **📝 Note**: 이 버전은 Flask로 구현된 프론트엔드입니다. Python 3.7+ 에서 안정적으로 작동합니다.

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

## 🚀 빠른 시작

### 필수 요구사항

- **Python**: 3.7 이상 (3.7, 3.8, 3.9, 3.10, 3.11 모두 지원)
- **Anthropic API Key**: [여기서 발급](https://console.anthropic.com/)

### 1️⃣ 환경 설정

```bash
# 백엔드 환경 설정
cd backend
cp .env.example .env

# .env 파일 편집하여 API 키 입력
# ANTHROPIC_API_KEY=your_api_key_here
```

### 2️⃣ 의존성 설치

**백엔드:**
```bash
cd backend
pip install -r requirements.txt
```

**프론트엔드:**
```bash
cd frontend
pip install -r requirements.txt
```

### 3️⃣ 실행

**방법 1: 스크립트 사용 (추천)**

터미널 1 - 백엔드:
```bash
./run_backend.sh
```

터미널 2 - 프론트엔드:
```bash
./run_frontend.sh
```

**방법 2: 직접 실행**

터미널 1 - 백엔드:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

터미널 2 - 프론트엔드:
```bash
cd frontend
python app.py
```

### 4️⃣ 사용

1. 브라우저에서 `http://localhost:5000` 접속
2. 원하는 내용 입력
3. AI가 자동으로 분석 및 프롬프트 생성
4. 생성된 프롬프트를 복사하여 사용

## 🏗️ 프로젝트 구조

```
prompt-engineering-automation/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── models/            # 데이터 모델
│   │   ├── services/          # 핵심 엔진
│   │   ├── config.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/                   # Flask 프론트엔드
│   ├── templates/             # HTML 템플릿
│   │   └── index.html
│   ├── static/                # 정적 파일
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── app.py                 # Flask 앱
│   └── requirements.txt
└── ...
```

## 🎨 프론트엔드 (Flask)

### 기술 스택
- **Flask**: 경량 웹 프레임워크
- **HTML/CSS/JavaScript**: 전통적인 웹 스택
- **Vanilla JS**: 프레임워크 없이 순수 JavaScript

### 주요 특징
- ✅ Python 3.7+ 모든 버전 지원
- ✅ 의존성 최소화 (Flask만 필요)
- ✅ 빠른 로딩 속도
- ✅ 반응형 디자인
- ✅ 단일 페이지 애플리케이션 (SPA)

### 화면 구성

1. **1단계 - 입력**: 사용자 쿼리 입력
2. **2단계 - 분석 확인**: AI 분석 결과 확인
3. **3단계 - 전략 선택**: 5가지 프롬프트 중 선택
4. **4단계 - 완성**: 최종 프롬프트 복사

## 📖 API 사용

### 프론트엔드 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | `/` | 메인 페이지 |
| GET | `/health` | 헬스 체크 |
| POST | `/api/analyze` | 쿼리 분석 (프록시) |
| POST | `/api/generate-prompts` | 프롬프트 생성 (프록시) |
| GET | `/api/strategies` | 전략 목록 (프록시) |

### 백엔드 API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎯 사용 예시

### 예시 1: 여행 블로그

**입력:**
```
겨울 서울 데이트 코스 블로그 글 써야 해
```

**AI 처리:**
1. 의도 파악: "콘텐츠 생성 / 블로그 / 20-30대 커플"
2. 트렌드 수집: "성수동 팝업스토어", "한강 야경 카페" 등
3. 5가지 프롬프트 생성
4. **Few-Shot 선택** → 감성적인 블로그 스타일

### 예시 2: 투자 분석

**입력:**
```
2025년 반도체 산업 투자 전망 분석
```

**AI 처리:**
1. 의도 파악: "분석 / 리포트 / 투자자"
2. 트렌드 수집: "AI칩 수요", "TSMC 실적" 등
3. 5가지 프롬프트 생성
4. **Structured 선택** → 체계적인 보고서 형식

## 🐛 문제 해결

### 백엔드 서버 연결 실패
```
문제: "백엔드 서버에 연결할 수 없습니다"
해결: 백엔드 서버 실행 확인
     ./run_backend.sh 또는
     cd backend && python -m uvicorn app.main:app --reload
```

### 프론트엔드 포트 충돌
```
문제: "Address already in use"
해결: 포트 5000이 사용 중입니다
     다른 포트 사용: python app.py --port 5001
     또는 app.py 파일에서 포트 변경
```

### API 키 오류
```
문제: "401 Unauthorized"
해결: backend/.env 파일에 올바른 ANTHROPIC_API_KEY 설정
```

### 모듈 없음 오류
```
문제: "ModuleNotFoundError"
해결: pip install -r requirements.txt
```

## 🔧 커스터마이징

### 프론트엔드 포트 변경

`frontend/app.py` 마지막 줄:
```python
app.run(debug=True, host="0.0.0.0", port=5000)  # 원하는 포트로 변경
```

### 백엔드 URL 변경

`frontend/app.py` 상단:
```python
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

환경 변수로 설정:
```bash
export API_BASE_URL=http://your-backend-url:8000
```

### 스타일 변경

`frontend/static/css/style.css`에서 CSS 변수 수정:
```css
:root {
    --primary-color: #667eea;  /* 원하는 색상으로 변경 */
    --secondary-color: #764ba2;
    ...
}
```

## 💡 장점

### Flask vs Streamlit

| 특징 | Flask | Streamlit |
|------|-------|-----------|
| Python 버전 | 3.7+ 모두 지원 | 3.8-3.11 권장 |
| 의존성 | 최소 | 많음 |
| 커스터마이징 | 높음 | 중간 |
| 로딩 속도 | 빠름 | 보통 |
| 학습 곡선 | 보통 | 쉬움 |

### Flask를 선택하는 이유

✅ **호환성**: Python 3.7 이상 모든 버전에서 작동
✅ **가벼움**: 최소한의 의존성
✅ **유연성**: HTML/CSS/JS를 직접 제어
✅ **프로덕션**: 실제 배포에 적합
✅ **성능**: 빠른 로딩 및 응답

## 🚀 배포

### Docker로 배포 (권장)

```bash
# Dockerfile 작성
# docker build -t prompt-engineering-app .
# docker run -p 5000:5000 -p 8000:8000 prompt-engineering-app
```

### 클라우드 배포

- **AWS**: EC2, Elastic Beanstalk
- **GCP**: Cloud Run, App Engine
- **Azure**: App Service
- **Heroku**: 간단한 배포

## 📚 문서

- **전체 문서**: [README.md](README.md)
- **빠른 시작**: [QUICKSTART.md](QUICKSTART.md)
- **프로젝트 요약**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 🤝 기여

버그 리포트, 기능 제안, Pull Request 환영합니다!

## 📝 라이선스

MIT License

---

**Made with ❤️ and AI**
