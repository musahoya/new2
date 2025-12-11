# 📋 프로젝트 요약

## 프롬프트 엔지니어링 자동화

### 🎯 프로젝트 목표
AI를 활용하여 최적화된 프롬프트를 자동으로 생성하는 웹 애플리케이션

### ✨ 핵심 기능
1. **자동 의도 파악**: 사용자 입력을 분석하여 의도, 키워드, 대상 독자 자동 식별
2. **트렌드 수집**: 최신 정보 자동 검색 및 정리 (10가지 핵심 트렌드)
3. **5가지 프롬프팅 전략**: CoT, Few-Shot, Meta, Self-Refine, Structured
4. **인터랙티브 UI**: Streamlit 기반의 직관적인 사용자 인터페이스

### 🏗️ 아키텍처

```
┌─────────────┐
│  사용자     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Streamlit Frontend  │ ← 프론트엔드 (포트 8501)
└──────┬──────────────┘
       │ HTTP
       ▼
┌─────────────────────┐
│  FastAPI Backend    │ ← 백엔드 API (포트 8000)
└──────┬──────────────┘
       │
       ├──→ IntentAnalyzer     (의도 파악)
       ├──→ TrendCollector     (트렌드 수집)
       ├──→ PromptGenerator    (프롬프트 생성)
       └──→ ConfirmationModule (사용자 확인)
       │
       ▼
┌─────────────────────┐
│  Anthropic Claude   │ ← AI 엔진
└─────────────────────┘
```

### 📁 프로젝트 구조

```
prompt-engineering-automation/
├── backend/                        # FastAPI 백엔드
│   ├── app/
│   │   ├── models/                # 데이터 모델
│   │   │   └── schemas.py
│   │   ├── services/              # 비즈니스 로직
│   │   │   ├── intent_analyzer.py
│   │   │   ├── trend_collector.py
│   │   │   ├── prompt_generator.py
│   │   │   └── confirmation_module.py
│   │   ├── config.py
│   │   └── main.py                # FastAPI 앱
│   └── requirements.txt
├── frontend/                       # Streamlit 프론트엔드
│   ├── app.py
│   └── requirements.txt
├── README.md                       # 전체 문서
├── QUICKSTART.md                   # 빠른 시작 가이드
├── run_backend.sh                  # 백엔드 실행 스크립트
├── run_frontend.sh                 # 프론트엔드 실행 스크립트
└── test_api.py                     # API 테스트 스크립트
```

### 🚀 실행 방법

**1. 백엔드 실행:**
```bash
./run_backend.sh
# 또는
cd backend && python -m uvicorn app.main:app --reload
```

**2. 프론트엔드 실행:**
```bash
./run_frontend.sh
# 또는
cd frontend && streamlit run app.py
```

**3. 테스트:**
```bash
python test_api.py
```

### 📊 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | `/` | API 정보 |
| GET | `/health` | 헬스 체크 |
| GET | `/api/strategies` | 사용 가능한 전략 목록 |
| POST | `/api/analyze` | 쿼리 분석 및 트렌드 수집 |
| POST | `/api/generate-prompts` | 프롬프트 생성 |
| POST | `/api/pipeline` | 전체 파이프라인 실행 |

### 🎨 프롬프팅 전략

1. **🧠 CoT (Chain of Thought)**
   - 논리적 단계별 사고
   - 용도: 복잡한 계획, 분석

2. **📝 Few-Shot Learning**
   - 예시를 통한 스타일 모방
   - 용도: 블로그, 에세이

3. **👨‍🏫 Meta-Prompting**
   - 전문가 페르소나
   - 용도: 객관적 분석, 리뷰

4. **🔄 Self-Refine**
   - 반복적 개선
   - 용도: 고퀄리티 콘텐츠

5. **📊 Structured Context**
   - 체계적 보고서
   - 용도: 데이터 분석, 리서치

### 🔧 기술 스택

**백엔드:**
- FastAPI
- Anthropic Claude API
- Pydantic
- Python 3.8+

**프론트엔드:**
- Streamlit
- Requests

### 🌟 주요 특징

✅ **자동화**: 수동으로 프롬프트를 작성할 필요 없음
✅ **최신 정보**: AI가 자동으로 트렌드 수집
✅ **다양한 전략**: 5가지 프롬프팅 기법 제공
✅ **사용자 친화적**: 직관적인 UI
✅ **즉시 사용**: 생성된 프롬프트를 바로 복사하여 사용

### 📈 확장 가능성

- [ ] 실제 웹 검색 API 연동 (Brave/Google)
- [ ] 데이터베이스 연동 (PostgreSQL)
- [ ] 사용자 히스토리 저장
- [ ] 프롬프트 템플릿 라이브러리
- [ ] 팀 협업 기능
- [ ] 커스텀 전략 추가
- [ ] 다국어 지원

### 🎓 학습 자료

- 전체 문서: [README.md](README.md)
- 빠른 시작: [QUICKSTART.md](QUICKSTART.md)
- API 문서: http://localhost:8000/docs

### 💡 사용 예시

**입력:**
```
"제주도 3박4일 여행 계획 짜줘"
```

**출력:**
- ✅ 의도 파악: 여행 가이드 작성
- ✅ 트렌드 수집: 제주도 핫플, 숨은 명소, 계절별 코스 등
- ✅ 5가지 프롬프트 생성
- ✅ 선택한 전략에 따른 최적화된 프롬프트 제공

### 🤝 기여

버그 리포트, 기능 제안, Pull Request 환영합니다!

### 📝 라이선스

MIT License

---

**개발 완료일**: 2025-12-11
**버전**: 1.0.0
