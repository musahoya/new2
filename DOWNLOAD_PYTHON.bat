@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   Python 다운로드 도우미                           ║
echo ╚════════════════════════════════════════════════════╝
echo.

echo Python 3.13을 사용 중이라 호환성 문제가 발생할 수 있습니다.
echo.
echo ════════════════════════════════════════════════════
echo  권장: Python 3.11.9 (가장 안정적)
echo ════════════════════════════════════════════════════
echo.
echo Python 3.11.9는:
echo ✅ 모든 패키지와 호환됩니다
echo ✅ 안정적이고 검증되었습니다
echo ✅ 대부분의 프로젝트에서 사용됩니다
echo.
echo ════════════════════════════════════════════════════
echo.
echo 어떤 버전을 다운로드할까요?
echo.
echo [1] Python 3.11.9 (권장)
echo [2] Python 3.12 (최신 안정)
echo [3] 취소
echo.

choice /c 123 /n /m "선택: "

if errorlevel 3 goto :END
if errorlevel 2 (
    echo.
    echo Python 3.12 다운로드 페이지를 엽니다...
    timeout /t 2 /nobreak >nul
    start https://www.python.org/downloads/release/python-3120/
    goto :INSTALL_GUIDE
)
if errorlevel 1 (
    echo.
    echo Python 3.11.9 다운로드 페이지를 엽니다...
    timeout /t 2 /nobreak >nul
    start https://www.python.org/downloads/release/python-3119/
    goto :INSTALL_GUIDE
)

:INSTALL_GUIDE
echo.
echo ════════════════════════════════════════════════════
echo  설치 방법
echo ════════════════════════════════════════════════════
echo.
echo 1. 다운로드 페이지에서 파일 선택:
echo    - Windows 64비트: "Windows installer (64-bit)"
echo    - Windows 32비트: "Windows installer (32-bit)"
echo.
echo 2. 다운로드한 파일 실행
echo.
echo 3. ⚠️  중요: "Add Python to PATH" 체크!
echo.
echo 4. "Install Now" 클릭
echo.
echo 5. 설치 완료 후 컴퓨터 재시작
echo.
echo 6. 다시 START.bat 실행
echo.
echo ════════════════════════════════════════════════════
echo.

:END
pause
