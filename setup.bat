@echo off
chcp 65001 > nul
echo ================================
echo   PDF 챗봇 시스템 설치
echo ================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo https://www.python.org/ 에서 Python 3.8 이상을 설치하세요.
    pause
    exit /b 1
)

echo [1/4] Python 버전 확인...
python --version

echo [2/4] 가상 환경 생성 중...
python -m venv venv

echo [3/4] 가상 환경 활성화 중...
call venv\Scripts\activate.bat

echo [4/4] 의존성 패키지 설치 중...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ================================
echo   ✅ 설치 완료!
echo ================================
echo.
echo 다음 단계:
echo 1. .env 파일을 생성하고 OPENAI_API_KEY를 설정하세요.
echo    예시:
echo    OPENAI_API_KEY=your_api_key_here
echo.
echo 2. run.bat 파일을 실행하여 서버를 시작하세요.
echo.
pause

