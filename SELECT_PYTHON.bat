@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   Python 버전 선택기                               ║
echo ╚════════════════════════════════════════════════════╝
echo.

echo 설치된 Python 버전 확인 중...
echo.

REM Python Launcher 사용 가능 여부 확인
where py >nul 2>&1
if errorlevel 1 (
    echo Python Launcher (py.exe)가 없습니다.
    echo 기본 python 명령어를 사용합니다.
    goto :USE_DEFAULT
)

echo 사용 가능한 Python 버전:
echo ════════════════════════════════════════════════════
py --list
echo ════════════════════════════════════════════════════
echo.

echo 어떤 Python을 사용하시겠습니까?
echo.
echo [1] Python 3.11 (권장)
echo [2] Python 3.13 (최신)
echo [3] 기본 Python
echo.

choice /c 123 /n /m "선택: "

if errorlevel 3 goto :USE_DEFAULT
if errorlevel 2 (
    echo.
    echo Python 3.13 선택됨
    echo py -3.13 > .python_version
    goto :DONE
)
if errorlevel 1 (
    echo.
    echo Python 3.11 선택됨
    echo py -3.11 > .python_version
    goto :DONE
)

:USE_DEFAULT
echo python > .python_version
echo.
echo 기본 Python 사용

:DONE
echo.
echo ════════════════════════════════════════════════════
echo  ✅ 설정 완료!
echo ════════════════════════════════════════════════════
echo.
echo 이제 START.bat를 실행하세요.
echo 선택한 Python 버전이 자동으로 사용됩니다.
echo.
pause
