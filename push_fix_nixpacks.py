#!/usr/bin/env python3
"""GitHub에 nixpacks 수정사항 push하는 스크립트"""
import subprocess
import os
import shutil
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """명령 실행"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류: {e}")
        if e.stdout:
            print(f"출력: {e.stdout}")
        if e.stderr:
            print(f"에러: {e.stderr}")
        return None

def main():
    print("🚀 GitHub Push 시작...")
    
    # 1. 임시 디렉토리에 레포 클론
    temp_dir = "/tmp/stock-push-nixpacks"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    print("📥 레포지토리 클론 중...")
    result = run_cmd(f"git clone https://github.com/BK-Korea/Reborn-to-Blackswan.git {temp_dir}")
    if result is None:
        print("❌ 클론 실패")
        return
    
    # 2. 수정된 파일 복사
    print("📋 파일 복사 중...")
    stock_dir = Path("/Users/bk/stock")
    target_dir = Path(temp_dir) / "stock"
    
    # nixpacks.toml 복사
    shutil.copy2(stock_dir / "nixpacks.toml", target_dir / "nixpacks.toml")
    print("  ✓ stock/nixpacks.toml 복사됨")
    
    # backend/nixpacks.toml 복사
    backend_target = target_dir / "backend"
    backend_target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(stock_dir / "backend" / "nixpacks.toml", backend_target / "nixpacks.toml")
    print("  ✓ stock/backend/nixpacks.toml 복사됨")
    
    # 3. Git 커밋 & Push
    print("💾 Git 커밋 중...")
    os.chdir(temp_dir)
    
    run_cmd("git add stock/nixpacks.toml stock/backend/nixpacks.toml")
    
    result = run_cmd('git commit -m "🔧 Fix Nixpacks: Remove ensurepip, use python311Full with pip directly"')
    if result is None:
        print("⚠️  커밋 실패 (변경사항이 없을 수 있음)")
        # 변경사항 확인
        status = run_cmd("git status")
        if status:
            print(f"Git 상태:\n{status}")
    else:
        print("  ✓ 커밋 완료")
    
    print("📤 GitHub에 Push 중...")
    result = run_cmd("git push origin main")
    if result is None:
        print("❌ Push 실패")
        return
    
    print("✅ Push 완료!")
    print(f"🔗 확인: https://github.com/BK-Korea/Reborn-to-Blackswan/tree/main/stock")
    
    # 4. 정리
    shutil.rmtree(temp_dir)
    print("🧹 임시 파일 정리 완료")

if __name__ == "__main__":
    main()

