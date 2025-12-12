@echo off
chcp 65001 >nul
echo ================================
echo 백엔드 서버 시작
echo ================================
echo.

cd /d "%~dp0backend"

REM .env 파일 확인
if not exist .env (
    echo [경고] .env 파일이 없습니다.
    echo .env.example을 복사하여 .env 파일을 생성합니다...
    copy .env.example .env
    echo.
    echo ================================
    echo ⚠️  중요: .env 파일을 열어서 API 키를 설정하세요!
    echo ================================
    echo.
    echo GOOGLE_GEMINI_API_KEY=발급받은_키
    echo.
    echo Google Gemini API 키 발급: https://aistudio.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

REM 의존성 설치 확인
echo [1/2] 의존성 확인 중...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [오류] 의존성 설치 실패
    pause
    exit /b 1
)

echo [2/2] 백엔드 서버 시작 중...
echo.
echo ✅ 백엔드 서버: http://localhost:8000
echo ✅ API 문서: http://localhost:8000/docs
echo.
echo 종료하려면 Ctrl+C를 누르세요.
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
