# 🚀 Quick Start Guide

프롬프트 엔지니어링 자동화 앱을 빠르게 시작하는 가이드입니다.

## ⚡ 5분 안에 시작하기

### 1. API 키 준비

[Anthropic Console](https://console.anthropic.com/)에서 API 키를 발급받으세요.

### 2. 환경 설정

```bash
# 백엔드 환경 설정
cd backend
cp .env.example .env

# .env 파일을 열어 API 키 입력
# ANTHROPIC_API_KEY=your_api_key_here
```

### 3. 의존성 설치

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

### 4. 실행

**방법 1: 스크립트 사용 (추천)**

터미널 1 (백엔드):
```bash
./run_backend.sh
```

터미널 2 (프론트엔드):
```bash
./run_frontend.sh
```

**방법 2: 직접 실행**

터미널 1 (백엔드):
```bash
cd backend
python -m uvicorn app.main:app --reload
```

터미널 2 (프론트엔드):
```bash
cd frontend
streamlit run app.py
```

### 5. 사용

1. 브라우저에서 `http://localhost:8501` 접속
2. 원하는 내용 입력
3. AI가 자동으로 분석 및 프롬프트 생성
4. 생성된 프롬프트를 복사하여 사용

## 🧪 테스트

백엔드가 제대로 작동하는지 확인:

```bash
python test_api.py
```

## 📖 API 문서

백엔드 API 문서는 다음에서 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 💡 사용 예시

### 예시 1: 블로그 글
```
입력: "겨울 서울 데이트 코스 추천 블로그 글"
→ AI가 최신 트렌드 수집
→ 5가지 프롬프트 생성
→ Few-Shot 전략 선택
→ 감성적인 블로그 스타일 프롬프트 제공
```

### 예시 2: 분석 보고서
```
입력: "2025년 AI 산업 트렌드 분석"
→ AI가 최신 정보 수집
→ 5가지 프롬프트 생성
→ Structured 전략 선택
→ 체계적인 보고서 형식 프롬프트 제공
```

## 🐛 문제 해결

### 서버 연결 실패
```
문제: "백엔드 서버에 연결할 수 없습니다"
해결: 백엔드 서버가 실행 중인지 확인
     ./run_backend.sh
```

### API 키 오류
```
문제: "401 Unauthorized"
해결: .env 파일에 올바른 ANTHROPIC_API_KEY 설정
```

### 모듈 없음 오류
```
문제: "ModuleNotFoundError: No module named 'anthropic'"
해결: pip install -r requirements.txt
```

## 🔧 설정 옵션

### 백엔드 포트 변경

`backend/app/config.py`:
```python
port: int = 8000  # 원하는 포트로 변경
```

### Claude 모델 변경

`backend/app/config.py`:
```python
claude_model: str = "claude-3-5-sonnet-20241022"  # 다른 모델로 변경
```

## 📚 다음 단계

- [전체 README](README.md) 읽기
- API 문서 탐색
- 프롬프트 전략 실험
- 웹 검색 API 연동 (선택사항)

## 🎉 즐겁게 사용하세요!

질문이나 문제가 있으면 이슈를 열어주세요.
