#!/bin/bash

# 프론트엔드 서버 실행 스크립트

echo "🎨 프론트엔드를 시작합니다..."
echo ""

# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치 확인
echo "📦 의존성을 확인합니다..."
pip install -r requirements.txt --quiet

echo ""
echo "✨ Streamlit 앱이 브라우저에서 열립니다."
echo "📍 주소: http://localhost:8501"
echo ""
echo "⚠️  백엔드 서버가 실행 중인지 확인하세요! (http://localhost:8000)"
echo ""

# Streamlit 실행
streamlit run app.py
