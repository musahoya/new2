@echo off
chcp 65001 >nul
title 프롬프트 엔지니어링 자동화

color 0A
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   프롬프트 엔지니어링 자동화 시스템                ║
echo ║   Prompt Engineering Automation                    ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo [단계 1] 환경 설정 확인 중...
echo.

cd /d "%~dp0"

REM .env 파일 확인
if not exist backend\.env (
    echo ❌ backend\.env 파일이 없습니다.
    echo.
    echo 지금 생성할까요? [Y/N]
    choice /c YN /n
    if errorlevel 2 goto :END

    copy backend\.env.example backend\.env
    echo.
    echo ✅ .env 파일이 생성되었습니다.
    echo.
    echo ════════════════════════════════════════════════════
    echo  ⚠️  중요: API 키를 설정해야 합니다!
    echo ════════════════════════════════════════════════════
    echo.
    echo 1. backend\.env 파일을 메모장으로 엽니다
    echo 2. GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
    echo    → 발급받은 API 키로 변경
    echo.
    echo 3. Google Gemini API 키 발급:
    echo    https://aistudio.google.com/app/apikey
    echo.
    echo 4. [선택] Brave Search API 키 발급:
    echo    https://brave.com/search/api/
    echo    (없어도 DuckDuckGo 무료 검색 사용)
    echo.
    echo ════════════════════════════════════════════════════
    echo.
    echo backend\.env 파일을 지금 열까요? [Y/N]
    choice /c YN /n
    if errorlevel 2 goto :INSTALL

    notepad backend\.env
    echo.
    echo API 키를 입력하고 저장했나요? [Y/N]
    choice /c YN /n
    if errorlevel 2 goto :END
)

:INSTALL
echo.
echo [단계 2] 의존성 설치 중...
echo.

echo [2-1] 백엔드 의존성 설치...
cd backend
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ 백엔드 의존성 설치 실패
    pause
    exit /b 1
)
cd ..

echo [2-2] 프론트엔드 의존성 설치...
cd frontend
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ 프론트엔드 의존성 설치 실패
    pause
    exit /b 1
)
cd ..

echo.
echo ✅ 모든 의존성 설치 완료!
echo.

:RUN
echo [단계 3] 서버 시작...
echo.
echo ════════════════════════════════════════════════════
echo  🚀 두 개의 터미널이 열립니다:
echo ════════════════════════════════════════════════════
echo  1. 백엔드 서버 (포트 8000)
echo  2. 프론트엔드 서버 (포트 5000)
echo.
echo  브라우저에서 http://localhost:5000 접속
echo ════════════════════════════════════════════════════
echo.

timeout /t 3 /nobreak >nul

REM 백엔드 서버 시작 (새 창)
start "백엔드 서버 (포트 8000)" cmd /k "cd /d %~dp0backend && echo 백엔드 서버 시작... && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 백엔드가 시작될 시간 대기
echo 백엔드 서버 시작 대기 중...
timeout /t 5 /nobreak >nul

REM 프론트엔드 서버 시작 (새 창)
start "프론트엔드 서버 (포트 5000)" cmd /k "cd /d %~dp0frontend && echo 프론트엔드 서버 시작... && python app.py"

REM 브라우저가 시작될 시간 대기
timeout /t 3 /nobreak >nul

REM 브라우저 자동 열기
echo.
echo 브라우저를 자동으로 열까요? [Y/N]
choice /c YN /n /t 5 /d Y
if errorlevel 2 goto :DONE

start http://localhost:5000

:DONE
echo.
echo ════════════════════════════════════════════════════
echo  ✅ 시스템이 시작되었습니다!
echo ════════════════════════════════════════════════════
echo.
echo  프론트엔드: http://localhost:5000
echo  백엔드 API: http://localhost:8000
echo  API 문서: http://localhost:8000/docs
echo.
echo  종료하려면 두 터미널 창을 닫으세요.
echo ════════════════════════════════════════════════════
echo.

:END
pause
