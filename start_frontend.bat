@echo off
chcp 65001 >nul
echo ================================
echo 프론트엔드 서버 시작
echo ================================
echo.

cd /d "%~dp0frontend"

REM 의존성 설치 확인
echo [1/2] 의존성 확인 중...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [오류] 의존성 설치 실패
    pause
    exit /b 1
)

echo [2/2] 프론트엔드 서버 시작 중...
echo.
echo ✅ 프론트엔드: http://localhost:5000
echo.
echo ⚠️  백엔드 서버가 먼저 실행되어 있어야 합니다!
echo    (start_backend.bat를 먼저 실행하세요)
echo.
echo 종료하려면 Ctrl+C를 누르세요.
echo.

python app.py

pause
