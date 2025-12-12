@echo off
chcp 65001 >nul
title 시스템 진단

color 0B
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   시스템 진단 도구                                  ║
echo ╚════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/5] Python 버전 확인
echo ════════════════════════════════════════════════════
python --version
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다!
    echo    https://www.python.org/downloads/ 에서 설치하세요.
    goto :ERROR
) else (
    echo ✅ Python 설치 확인
)
echo.

echo [2/5] .env 파일 확인
echo ════════════════════════════════════════════════════
if exist backend\.env (
    echo ✅ backend\.env 파일 존재

    REM API 키 설정 확인
    findstr /C:"GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here" backend\.env >nul
    if errorlevel 1 (
        echo ✅ Google Gemini API 키 설정됨
    ) else (
        echo ❌ Google Gemini API 키가 기본값입니다!
        echo    backend\.env 파일을 열어 실제 API 키로 변경하세요.
        echo.
        echo    발급: https://aistudio.google.com/app/apikey
        goto :ERROR
    )
) else (
    echo ❌ backend\.env 파일이 없습니다!
    echo    START.bat를 실행하여 자동 생성하세요.
    goto :ERROR
)
echo.

echo [3/5] 백엔드 의존성 확인
echo ════════════════════════════════════════════════════
cd backend
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo ❌ 백엔드 의존성이 설치되지 않았습니다.
    echo    자동 설치할까요? [Y/N]
    choice /c YN /n
    if errorlevel 2 goto :SKIP_BACKEND

    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 설치 실패
        goto :ERROR
    )
    echo ✅ 설치 완료
) else (
    echo ✅ 백엔드 의존성 설치 확인
)
cd ..
echo.

:SKIP_BACKEND
echo [4/5] 프론트엔드 의존성 확인
echo ════════════════════════════════════════════════════
cd frontend
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ❌ 프론트엔드 의존성이 설치되지 않았습니다.
    echo    자동 설치할까요? [Y/N]
    choice /c YN /n
    if errorlevel 2 goto :SKIP_FRONTEND

    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 설치 실패
        goto :ERROR
    )
    echo ✅ 설치 완료
) else (
    echo ✅ 프론트엔드 의존성 설치 확인
)
cd ..
echo.

:SKIP_FRONTEND
echo [5/5] 포트 사용 확인
echo ════════════════════════════════════════════════════
netstat -ano | findstr :8000 >nul
if errorlevel 1 (
    echo ✅ 포트 8000 사용 가능 (백엔드)
) else (
    echo ⚠️  포트 8000이 이미 사용 중입니다 (백엔드)
    echo    다른 프로그램을 종료하거나 다른 포트를 사용하세요.
)

netstat -ano | findstr :5000 >nul
if errorlevel 1 (
    echo ✅ 포트 5000 사용 가능 (프론트엔드)
) else (
    echo ⚠️  포트 5000이 이미 사용 중입니다 (프론트엔드)
    echo    다른 프로그램을 종료하거나 다른 포트를 사용하세요.
)
echo.

echo ════════════════════════════════════════════════════
echo  ✅ 진단 완료!
echo ════════════════════════════════════════════════════
echo.
echo  시스템을 시작하려면 START.bat를 실행하세요.
echo.
goto :END

:ERROR
echo.
echo ════════════════════════════════════════════════════
echo  ❌ 문제가 발견되었습니다!
echo ════════════════════════════════════════════════════
echo.
echo  위의 오류를 해결한 후 다시 시도하세요.
echo.

:END
pause
