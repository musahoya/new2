@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 프롬프트 엔지니어링 자동화

color 0A
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   프롬프트 엔지니어링 자동화 시스템                ║
echo ║   Prompt Engineering Automation                    ║
echo ╚════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Python 버전 선택 확인
if exist .python_version (
    set /p PYTHON_CMD=<.python_version
    echo Python 명령어: !PYTHON_CMD!
) else (
    REM py launcher 시도
    where py >nul 2>&1
    if errorlevel 1 (
        set PYTHON_CMD=python
    ) else (
        REM Python 3.11 우선 시도
        py -3.11 --version >nul 2>&1
        if errorlevel 1 (
            set PYTHON_CMD=python
        ) else (
            set PYTHON_CMD=py -3.11
            echo ✅ Python 3.11 자동 감지
        )
    )
)

echo.
echo [단계 1] 환경 설정 확인 중...
echo.

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

REM Python 버전 확인
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 사용 중인 Python: %PYTHON_VERSION%
echo.

REM Python 3.13 경고
echo %PYTHON_VERSION% | findstr /C:"3.13" >nul
if not errorlevel 1 (
    echo ⚠️  Python 3.13 감지! 호환성 문제가 있을 수 있습니다.
    echo    Python 3.11 권장 - https://www.python.org/downloads/release/python-3119/
    echo.
    echo    SELECT_PYTHON.bat 실행하여 버전 변경 가능
    timeout /t 3 /nobreak >nul
)

echo [2-1] pip 업그레이드...
%PYTHON_CMD% -m pip install --upgrade pip --quiet 2>nul

echo [2-2] 백엔드 의존성 설치...
cd backend
%PYTHON_CMD% -m pip install --upgrade setuptools wheel --quiet 2>nul
%PYTHON_CMD% -m pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo.
    echo ════════════════════════════════════════════════════
    echo  ❌ 백엔드 의존성 설치 실패!
    echo ════════════════════════════════════════════════════
    echo.
    echo Python 3.13 호환성 문제일 수 있습니다.
    echo.
    echo 해결 방법:
    echo [1] Python 3.11 설치 (가장 권장)
    echo     https://www.python.org/downloads/release/python-3119/
    echo.
    echo [2] INSTALL.bat 실행 (자동 진단)
    echo.
    echo [3] 관리자 권한으로 실행
    echo     이 파일 우클릭 → "관리자 권한으로 실행"
    echo.
    echo ════════════════════════════════════════════════════
    pause
    exit /b 1
)
cd ..

echo [2-3] 프론트엔드 의존성 설치...
cd frontend
%PYTHON_CMD% -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ 프론트엔드 의존성 설치 실패
    echo    (보통 백엔드만 설치되면 괜찮습니다)
    timeout /t 2 /nobreak >nul
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
start "백엔드 서버 (포트 8000)" cmd /k "cd /d %~dp0backend && echo 백엔드 서버 시작... && %PYTHON_CMD% -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 백엔드가 시작될 시간 대기
echo 백엔드 서버 시작 대기 중...
timeout /t 5 /nobreak >nul

REM 프론트엔드 서버 시작 (새 창)
start "프론트엔드 서버 (포트 5000)" cmd /k "cd /d %~dp0frontend && echo 프론트엔드 서버 시작... && %PYTHON_CMD% app.py"

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
