#!/bin/bash
# GitHub에 수정사항 push하는 스크립트

echo "🚀 GitHub Push 시작..."

# 임시 디렉토리에 레포 클론
TEMP_DIR="/tmp/stock-push-fix"
rm -rf "$TEMP_DIR"
git clone https://github.com/BK-Korea/Reborn-to-Blackswan.git "$TEMP_DIR"

# 파일 복사
echo "📋 파일 복사 중..."
cp /Users/bk/stock/nixpacks.toml "$TEMP_DIR/stock/nixpacks.toml"
cp /Users/bk/stock/backend/nixpacks.toml "$TEMP_DIR/stock/backend/nixpacks.toml"
echo "  ✓ 파일 복사 완료"

# Git 커밋 & Push
cd "$TEMP_DIR"
git add stock/nixpacks.toml stock/backend/nixpacks.toml
git commit -m "🔧 Fix Nixpacks: Use python311Full and ensurepip for pip installation" || echo "⚠️  커밋 실패 (변경사항이 없을 수 있음)"

echo "📤 GitHub에 Push 중..."
git push origin main

echo "✅ 완료!"
echo "🔗 확인: https://github.com/BK-Korea/Reborn-to-Blackswan/tree/main/stock"

# 정리
rm -rf "$TEMP_DIR"
echo "🧹 임시 파일 정리 완료"

