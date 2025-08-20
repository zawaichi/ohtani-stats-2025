#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
バッチ処理テストスクリプト
手動でバッチ更新を実行してテスト
"""

import os
import sys
import subprocess
from datetime import datetime

def test_batch():
    """バッチ処理をテスト実行"""
    print("🧪 バッチ処理テスト開始")
    print("=" * 50)
    
    # バッチスクリプトの存在確認
    batch_script = 'daily_update_batch.py'
    if not os.path.exists(batch_script):
        print(f"❌ バッチスクリプトが見つかりません: {batch_script}")
        return False
    
    # 実行前の状態確認
    print("📊 実行前の状態:")
    print(f"  現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  バッチスクリプト: {batch_script}")
    
    # バッチ処理を実行
    print("\n🔄 バッチ処理を実行中...")
    try:
        result = subprocess.run([sys.executable, batch_script], 
                              capture_output=True, text=True, encoding='utf-8')
        
        print("📝 実行結果:")
        print(f"  終了コード: {result.returncode}")
        
        if result.stdout:
            print("  標準出力:")
            for line in result.stdout.strip().split('\n'):
                print(f"    {line}")
        
        if result.stderr:
            print("  エラー出力:")
            for line in result.stderr.strip().split('\n'):
                print(f"    {line}")
        
        if result.returncode == 0:
            print("\n✅ バッチ処理が正常に完了しました")
            return True
        else:
            print("\n❌ バッチ処理でエラーが発生しました")
            return False
            
    except Exception as e:
        print(f"\n❌ バッチ処理実行エラー: {str(e)}")
        return False

def check_logs():
    """ログファイルを確認"""
    print("\n📋 ログファイル確認:")
    log_file = 'logs/daily_update.log'
    
    if os.path.exists(log_file):
        print(f"  ログファイル: {log_file}")
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"  ログ行数: {len(lines)}")
                if lines:
                    print("  最新のログ:")
                    for line in lines[-5:]:  # 最新5行を表示
                        print(f"    {line.strip()}")
        except Exception as e:
            print(f"  ログ読み込みエラー: {e}")
    else:
        print(f"  ログファイルが見つかりません: {log_file}")

def main():
    """メイン処理"""
    print("🚀 大谷翔平成績データ バッチ処理テスト")
    print("=" * 50)
    
    # バッチ処理テスト
    success = test_batch()
    
    # ログ確認
    check_logs()
    
    # 結果表示
    print("\n" + "=" * 50)
    if success:
        print("🎉 テスト完了: バッチ処理は正常に動作しています")
    else:
        print("⚠️  テスト完了: バッチ処理で問題が発生しました")
    
    print("\n💡 次のステップ:")
    print("1. テストが成功した場合: python3 setup_scheduler.py setup")
    print("2. cronジョブの確認: python3 setup_scheduler.py check")
    print("3. 手動実行: python3 daily_update_batch.py")

if __name__ == '__main__':
    main()
