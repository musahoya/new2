@echo off
chcp 65001 >nul
echo.
echo ════════════════════════════════════════════════════
echo   간편 설치 테스트 (에러 메시지 전체 표시)
echo ════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

REM Python 명령어 설정
set PYTHON_CMD=python

REM py launcher로 Python 3.11 확인
where py >nul 2>&1
if not errorlevel 1 (
    py -3.11 --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=py -3.11
        echo ✅ Python 3.11 사용
    )
)

echo.
echo Python 버전 확인:
%PYTHON_CMD% --version
echo.

echo ════════════════════════════════════════════════════
echo [1/4] pip 업그레이드
echo ════════════════════════════════════════════════════
%PYTHON_CMD% -m pip install --upgrade pip
echo.

echo ════════════════════════════════════════════════════
echo [2/4] setuptools, wheel 설치
echo ════════════════════════════════════════════════════
%PYTHON_CMD% -m pip install --upgrade setuptools wheel
echo.

echo ════════════════════════════════════════════════════
echo [3/4] 백엔드 패키지 설치
echo ════════════════════════════════════════════════════
cd backend
%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ 백엔드 패키지 설치 실패!
    echo.
    echo 위의 에러 메시지를 확인하고 스크린샷 찍어주세요.
    pause
    exit /b 1
)
cd ..
echo.

echo ════════════════════════════════════════════════════
echo [4/4] 프론트엔드 패키지 설치
echo ════════════════════════════════════════════════════
cd frontend
%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo ⚠️  프론트엔드 설치 실패 (보통 괜찮습니다)
)
cd ..
echo.

echo ════════════════════════════════════════════════════
echo  ✅ 설치 완료!
echo ════════════════════════════════════════════════════
echo.
echo 이제 START.bat를 실행하세요.
echo.
pause
