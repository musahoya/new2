#!/bin/bash

# 백엔드 서버 실행 스크립트

echo "🚀 백엔드 서버를 시작합니다..."
echo ""

# 백엔드 디렉토리로 이동
cd backend

# .env 파일 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다."
    echo "📝 .env.example을 복사하여 .env 파일을 생성합니다..."
    cp .env.example .env
    echo ""
    echo "✅ .env 파일이 생성되었습니다."
    echo "⚠️  .env 파일을 열어 ANTHROPIC_API_KEY를 설정해주세요!"
    echo ""
    exit 1
fi

# 의존성 설치 확인
echo "📦 의존성을 확인합니다..."
pip install -r requirements.txt --quiet

echo ""
echo "✨ 백엔드 서버가 http://localhost:8000 에서 실행됩니다."
echo "📖 API 문서: http://localhost:8000/docs"
echo ""

# 서버 실행
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
