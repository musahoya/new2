@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   Python 버전 확인 및 패키지 설치                  ║
echo ╚════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0backend"

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

REM Python 버전 확인
echo [1/3] Python 버전 확인 중...
echo.

%PYTHON_CMD% --version
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다!
    echo.
    echo https://www.python.org/downloads/ 에서 설치하세요.
    echo 권장 버전: Python 3.11 (안정적)
    pause
    exit /b 1
)

REM Python 버전 추출
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version') do set PYTHON_VERSION=%%i
echo Python 버전: %PYTHON_VERSION%
echo.

REM Python 3.13 체크
echo %PYTHON_VERSION% | findstr /C:"3.13" >nul
if not errorlevel 1 (
    echo ⚠️  Python 3.13을 사용하고 계십니다.
    echo.
    echo Python 3.13은 매우 최신 버전이라 일부 패키지가 호환되지 않을 수 있습니다.
    echo.
    echo 다음 중 하나를 선택하세요:
    echo.
    echo [1] 최신 버전으로 설치 시도 (권장)
    echo [2] Python 3.11 다운로드 페이지 열기
    echo [3] 취소
    echo.
    choice /c 123 /n /m "선택: "

    if errorlevel 3 goto :END
    if errorlevel 2 (
        start https://www.python.org/downloads/release/python-3119/
        echo.
        echo Python 3.11 다운로드 페이지가 열렸습니다.
        echo 설치 후 다시 실행해주세요.
        pause
        exit /b 1
    )
)

echo [2/3] pip 업그레이드 중...
%PYTHON_CMD% -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo ⚠️  pip 업그레이드 실패 (무시하고 계속)
)
echo.

echo [3/3] 패키지 설치 중...
echo.
echo 이 작업은 1-2분 정도 걸릴 수 있습니다...
echo.

REM 먼저 기본 패키지 설치
%PYTHON_CMD% -m pip install --upgrade setuptools wheel --quiet

REM requirements.txt 설치
%PYTHON_CMD% -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ════════════════════════════════════════════════════
    echo  ❌ 설치 실패!
    echo ════════════════════════════════════════════════════
    echo.
    echo 가능한 해결 방법:
    echo.
    echo [방법 1] Python 3.11 설치 (권장)
    echo   - 가장 안정적인 버전
    echo   - https://www.python.org/downloads/release/python-3119/
    echo.
    echo [방법 2] Visual C++ Build Tools 설치
    echo   - 일부 패키지는 C 컴파일러가 필요합니다
    echo   - https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo [방법 3] 관리자 권한으로 실행
    echo   - 배치 파일을 우클릭 → "관리자 권한으로 실행"
    echo.
    echo ════════════════════════════════════════════════════
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════
echo  ✅ 설치 완료!
echo ════════════════════════════════════════════════════
echo.
echo 이제 START.bat를 실행하여 시스템을 시작하세요.
echo.

pause
