#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スケジューラー設定スクリプト
毎日日本時間14時にバッチ更新を実行するcronジョブを設定
"""

import os
import subprocess
import sys

def setup_cron_job():
    """cronジョブを設定"""
    try:
        # 現在のディレクトリの絶対パスを取得
        current_dir = os.path.abspath('.')
        python_path = sys.executable
        batch_script = os.path.join(current_dir, 'daily_update_batch.py')
        
        # cronジョブの内容（毎日14時に実行）
        cron_job = f"0 14 * * * cd {current_dir} && {python_path} {batch_script} >> {current_dir}/logs/cron.log 2>&1"
        
        # 既存のcronジョブを確認
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        existing_crons = result.stdout if result.returncode == 0 else ""
        
        # 既に同じジョブが存在するかチェック
        if batch_script in existing_crons:
            print("⚠️  既に同じcronジョブが設定されています")
            return False
        
        # 新しいcronジョブを追加
        new_crons = existing_crons + "\n" + cron_job + "\n"
        
        # 一時ファイルに書き込み
        with open('/tmp/new_crontab', 'w') as f:
            f.write(new_crons)
        
        # crontabに適用
        subprocess.run(['crontab', '/tmp/new_crontab'], check=True)
        
        # 一時ファイルを削除
        os.remove('/tmp/new_crontab')
        
        print("✅ cronジョブが正常に設定されました")
        print(f"📅 実行時間: 毎日14:00 (日本時間)")
        print(f"📁 実行スクリプト: {batch_script}")
        print(f"📝 ログファイル: {current_dir}/logs/daily_update.log")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ cronジョブ設定エラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

def check_cron_status():
    """cronジョブの状態を確認"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📋 現在のcronジョブ:")
            print(result.stdout)
        else:
            print("📋 設定されているcronジョブはありません")
            
    except Exception as e:
        print(f"❌ cronジョブ確認エラー: {e}")

def remove_cron_job():
    """cronジョブを削除"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            existing_crons = result.stdout
            current_dir = os.path.abspath('.')
            batch_script = os.path.join(current_dir, 'daily_update_batch.py')
            
            # 該当するジョブを除外
            filtered_crons = []
            for line in existing_crons.split('\n'):
                if batch_script not in line and line.strip():
                    filtered_crons.append(line)
            
            # 新しいcrontabを設定
            new_crons = '\n'.join(filtered_crons) + '\n'
            
            with open('/tmp/new_crontab', 'w') as f:
                f.write(new_crons)
            
            subprocess.run(['crontab', '/tmp/new_crontab'], check=True)
            os.remove('/tmp/new_crontab')
            
            print("✅ cronジョブが削除されました")
            return True
            
    except Exception as e:
        print(f"❌ cronジョブ削除エラー: {e}")
        return False

def main():
    """メイン処理"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'setup':
            setup_cron_job()
        elif command == 'check':
            check_cron_status()
        elif command == 'remove':
            remove_cron_job()
        else:
            print("使用方法:")
            print("  python3 setup_scheduler.py setup   - cronジョブを設定")
            print("  python3 setup_scheduler.py check   - cronジョブを確認")
            print("  python3 setup_scheduler.py remove  - cronジョブを削除")
    else:
        print("🚀 大谷翔平成績データ 自動更新スケジューラー")
        print("=" * 50)
        print("1. スケジューラー設定")
        print("2. 現在の設定確認")
        print("3. スケジューラー削除")
        print("4. 終了")
        
        choice = input("\n選択してください (1-4): ")
        
        if choice == '1':
            setup_cron_job()
        elif choice == '2':
            check_cron_status()
        elif choice == '3':
            remove_cron_job()
        elif choice == '4':
            print("終了します")
        else:
            print("無効な選択です")

if __name__ == '__main__':
    main()
