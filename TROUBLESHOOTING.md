# 🐛 문제 해결 가이드

## Python 3.13 호환성 문제

### 증상
```
error: metadata-generation-failed
× Encountered error while generating package metadata.
```

### 원인
Python 3.13은 2024년 10월에 출시된 **매우 최신 버전**이라, 일부 패키지들이 아직 완벽히 지원하지 않습니다.

### 해결 방법

#### ✅ 방법 1: Python 3.11 설치 (가장 권장)

1. **DOWNLOAD_PYTHON.bat** 더블클릭
2. Python 3.11.9 선택
3. 다운로드 및 설치
4. **중요: "Add Python to PATH" 체크!**
5. 컴퓨터 재시작
6. START.bat 다시 실행

**Python 3.11을 권장하는 이유:**
- ✅ 모든 패키지와 100% 호환
- ✅ 안정적이고 검증됨
- ✅ 대부분의 프로젝트에서 사용

#### ⚙️ 방법 2: INSTALL.bat 실행

```
INSTALL.bat 더블클릭
→ 자동으로 최신 버전 시도
```

#### 🔧 방법 3: 관리자 권한으로 실행

1. START.bat 우클릭
2. "관리자 권한으로 실행" 선택

---

## 백엔드 서버 연결 실패

### 증상
```
백엔드 서버에 연결할 수 없습니다
503 Service Unavailable
```

### 원인
백엔드 서버가 실행되지 않음

### 해결 방법

#### ✅ 방법 1: CHECK.bat 실행

```
CHECK.bat 더블클릭
→ 자동 진단 및 문제 해결
```

#### ✅ 방법 2: 수동 확인

1. **백엔드 터미널 확인**
   - 백엔드 터미널 창이 열려 있나요?
   - 에러 메시지가 있나요?

2. **.env 파일 확인**
   ```
   backend\.env 파일 열기
   GOOGLE_GEMINI_API_KEY=실제_API_키_입력
   ```

3. **포트 8000 확인**
   ```
   명령 프롬프트:
   netstat -ano | findstr :8000
   ```

---

## API 키 관련 문제

### 증상
```
API 키 오류
401 Unauthorized
```

### 해결 방법

1. **backend\.env 파일 열기**
2. 다음 확인:
   ```
   GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. `your_gemini_api_key_here`를 **실제 API 키**로 변경
4. 저장
5. 백엔드 재시작 (Ctrl+C 후 다시 START.bat)

**API 키 발급:**
https://aistudio.google.com/app/apikey

---

## 포트 사용 중 에러

### 증상
```
Address already in use
포트 8000 또는 5000이 이미 사용 중
```

### 해결 방법

#### 방법 1: 다른 프로그램 종료

1. 작업 관리자 열기 (Ctrl+Shift+Esc)
2. Python 프로세스 모두 종료
3. 다시 실행

#### 방법 2: 포트 변경

**backend/app/config.py:**
```python
port: int = 8001  # 8000 → 8001로 변경
```

**frontend/app.py:**
```python
app.run(debug=True, host="0.0.0.0", port=5001)  # 5000 → 5001
```

---

## 의존성 설치 실패

### 증상
```
pip install 실패
모듈 없음 오류
```

### 해결 방법

#### 방법 1: INSTALL.bat 실행
```
INSTALL.bat 더블클릭
```

#### 방법 2: 수동 설치

```bash
cd backend
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

#### 방법 3: Visual C++ Build Tools 설치

일부 패키지는 C 컴파일러가 필요합니다.

1. https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. "Build Tools" 다운로드
3. "C++ build tools" 선택하여 설치

---

## Python 버전 확인

### 현재 Python 버전 확인

```bash
python --version
```

### 권장 버전

| 버전 | 상태 | 추천 |
|------|------|------|
| Python 3.13 | ⚠️  너무 최신 | ❌ |
| Python 3.12 | ✅ 안정 | ⚡ 괜찮음 |
| Python 3.11 | ✅ 매우 안정 | ⭐ **강력 추천** |
| Python 3.10 | ✅ 안정 | ⭐ 추천 |
| Python 3.9 | ✅ 안정 | ✅ 가능 |
| Python 3.8 | ⚠️  구버전 | ⚠️  |
| Python 3.7 | ⚠️  구버전 | ⚠️  |

---

## 자주 묻는 질문

### Q: Python 3.13을 꼭 바꿔야 하나요?

**A:** 권장합니다. Python 3.11이 가장 안정적입니다.

하지만 시도해볼 수 있습니다:
1. INSTALL.bat 실행
2. 최신 버전으로 설치 시도

### Q: Python을 여러 버전 설치해도 되나요?

**A:** 네, 가능합니다. 여러 버전을 동시에 설치할 수 있습니다.

### Q: 비용이 드나요?

**A:** 무료입니다!
- Google Gemini API: 무료 할당량
- DuckDuckGo 검색: 완전 무료
- Brave Search (선택): 2,000회/월 무료

### Q: 백엔드와 프론트엔드를 따로 실행해야 하나요?

**A:** START.bat는 자동으로 둘 다 실행합니다.

---

## 빠른 진단 체크리스트

□ Python 3.11 또는 3.12 설치?
□ backend\.env 파일 존재?
□ API 키 설정 완료?
□ 의존성 설치 완료?
□ 백엔드 터미널 실행 중?
□ 포트 8000, 5000 사용 가능?

**모두 체크되면 START.bat 실행!**

---

## 도움이 필요하면

1. **CHECK.bat** - 자동 진단
2. **INSTALL.bat** - 의존성 재설치
3. **DOWNLOAD_PYTHON.bat** - Python 다운로드

---

**문제가 계속되면 GitHub Issues에 남겨주세요!**
