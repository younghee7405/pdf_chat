#!/bin/bash

echo "================================"
echo "  PDF 챗봇 시스템 시작"
echo "================================"
echo ""

# 가상 환경 활성화 확인
if [ -f "venv/bin/activate" ]; then
    echo "[1/3] 가상 환경 활성화 중..."
    source venv/bin/activate
else
    echo "⚠️  가상 환경을 찾을 수 없습니다."
    echo "먼저 'python3 -m venv venv' 명령으로 가상 환경을 생성하세요."
    exit 1
fi

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env 파일을 찾을 수 없습니다."
    echo ".env 파일을 생성하고 OPENAI_API_KEY를 설정하세요."
    echo ""
    exit 1
fi

echo "[2/3] 필요한 디렉토리 생성 중..."
mkdir -p uploads
mkdir -p static/page_images
mkdir -p vector_store

echo "[3/3] Flask 서버 시작 중..."
echo ""
echo "✅ 준비 완료! 브라우저에서 http://localhost:5000 으로 접속하세요."
echo ""
echo "⏹️  종료하려면 Ctrl+C를 누르세요."
echo ""
echo "================================"
echo ""

python app.py

