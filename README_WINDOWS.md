# 🚀 Windows 간단 시작 가이드

> **Windows 사용자를 위한 초간단 실행 가이드**

## ⚡ 3단계로 시작하기

### 1️⃣ Google Gemini API 키 발급 (무료)

1. https://aistudio.google.com/app/apikey 접속
2. **Get API Key** 클릭
3. API 키 복사

### 2️⃣ 파일 다운로드 및 압축 해제

GitHub에서 다운로드한 파일을 압축 해제합니다.

### 3️⃣ START.bat 더블클릭!

```
📁 new2/
  └─ START.bat  ← 이 파일을 더블클릭!
```

**끝!** 브라우저가 자동으로 열립니다.

---

## 🎯 실행 방법

### 방법 1: 자동 실행 (추천 ⭐⭐⭐)

```
START.bat 더블클릭
  ↓
API 키 입력 (첫 실행시만)
  ↓
자동으로 모든 것 실행
  ↓
브라우저가 자동으로 열림
```

### 방법 2: 수동 실행

**터미널 1 - 백엔드:**
```
start_backend.bat 더블클릭
```

**터미널 2 - 프론트엔드:**
```
start_frontend.bat 더블클릭
```

---

## 🐛 문제 해결

### "백엔드 서버에 연결할 수 없습니다" 에러

**해결:**
```
CHECK.bat 더블클릭
  ↓
문제 자동 진단
  ↓
화면의 지시대로 수정
```

### API 키 설정 확인

1. `backend/.env` 파일을 메모장으로 열기
2. 다음 줄 확인:
   ```
   GOOGLE_GEMINI_API_KEY=여기에_실제_API_키
   ```
3. `your_gemini_api_key_here` 부분을 실제 API 키로 변경

### Python이 설치되지 않음

https://www.python.org/downloads/ 에서 설치
- Python 3.7 이상 필요
- 설치 시 "Add Python to PATH" 체크!

---

## 📁 배치 파일 설명

| 파일 | 설명 |
|------|------|
| **START.bat** | 🚀 모든 것을 자동 실행 (추천) |
| **CHECK.bat** | 🔍 시스템 진단 및 문제 해결 |
| start_backend.bat | 백엔드만 실행 |
| start_frontend.bat | 프론트엔드만 실행 |

---

## 💡 사용 팁

### 1. 첫 실행 시
```
1. START.bat 더블클릭
2. API 키 입력
3. 끝!
```

### 2. 두 번째 실행부터
```
START.bat 더블클릭만 하면 됩니다!
```

### 3. 에러 발생 시
```
CHECK.bat 더블클릭 → 자동 진단
```

---

## 🎯 간단 사용법

1. **START.bat 실행**
2. **브라우저에서 자동으로 열림**
3. **쿼리 입력**
   ```
   예: "제주도 3박4일 여행 계획"
   예: "블로그 글 작성 팁"
   ```
4. **AI가 자동으로:**
   - 의도 파악
   - 최신 트렌드 수집 (DuckDuckGo 무료 검색)
   - 5가지 프롬프트 생성
5. **원하는 프롬프트 선택**
6. **복사해서 ChatGPT/Claude에 사용!**

---

## 🌟 무료 기능

✅ **Google Gemini API**: 무료 할당량
✅ **DuckDuckGo 검색**: 완전 무료, 무제한
✅ **선택사항 - Brave Search**: 2,000회/월 무료

**총 비용: $0/월** (무료 할당량 내)

---

## 📞 도움말

### 자주 묻는 질문

**Q: Python이 없어요!**
A: https://www.python.org/downloads/ 설치

**Q: API 키는 어디서 받나요?**
A: https://aistudio.google.com/app/apikey

**Q: 백엔드가 안 열려요!**
A: CHECK.bat 실행 → 문제 자동 진단

**Q: 비용이 드나요?**
A: 무료! (Gemini + DuckDuckGo 무료)

---

## ✅ 시스템 요구사항

- Windows 7 이상
- Python 3.7 이상
- 인터넷 연결

---

## 🎉 시작하기

```
1. START.bat 더블클릭
2. 끝!
```

**그게 전부입니다!** 🚀

---

## 📚 더 자세한 정보

- **전체 문서**: README.md
- **빠른 시작**: QUICKSTART.md
- **Flask 버전**: README_FLASK.md
