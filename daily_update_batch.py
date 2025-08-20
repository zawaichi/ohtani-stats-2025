#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大谷翔平成績データ 日次更新バッチ
毎日日本時間14時にデータを自動更新
"""

import os
import sys
import logging
from datetime import datetime, timezone, timedelta
import subprocess
import time

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/daily_update.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def get_jst_time():
    """日本時間を取得"""
    utc_time = datetime.now(timezone.utc)
    jst_time = utc_time.astimezone(timezone(timedelta(hours=9)))
    return jst_time

def run_update_script(script_name, description):
    """更新スクリプトを実行"""
    try:
        logging.info(f"🔄 {description}を開始: {script_name}")
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            logging.info(f"✅ {description}完了: {script_name}")
            if result.stdout:
                logging.info(f"出力: {result.stdout.strip()}")
        else:
            logging.error(f"❌ {description}エラー: {script_name}")
            logging.error(f"エラー出力: {result.stderr}")
            return False
            
    except Exception as e:
        logging.error(f"❌ {description}実行エラー: {script_name} - {str(e)}")
        return False
    
    return True

def daily_update():
    """日次更新処理"""
    jst_time = get_jst_time()
    logging.info(f"🚀 日次更新バッチ開始 - {jst_time.strftime('%Y-%m-%d %H:%M:%S JST')}")
    
    # 必要なディレクトリを作成
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    success_count = 0
    total_count = 0
    
    # 更新スクリプトのリスト
    update_scripts = [
        ('fetch_dodgers_games.py', 'ドジャース試合データ取得'),
        ('create_home_run_chart_comparison.py', 'ホームラン比較データ生成'),
        ('create_home_run_prediction.py', 'ホームラン予測データ生成'),
        ('create_home_run_with_prediction.py', 'ホームラン予測統合データ生成')
    ]
    
    # 各スクリプトを実行
    for script_name, description in update_scripts:
        total_count += 1
        if run_update_script(script_name, description):
            success_count += 1
    
    # 結果ログ
    logging.info(f"📊 更新結果: {success_count}/{total_count} 成功")
    
    if success_count == total_count:
        logging.info("🎉 全ての更新が正常に完了しました")
        return True
    else:
        logging.warning(f"⚠️ 一部の更新でエラーが発生しました ({total_count - success_count}件)")
        return False

def main():
    """メイン処理"""
    try:
        success = daily_update()
        if success:
            logging.info("✅ 日次更新バッチ正常終了")
            sys.exit(0)
        else:
            logging.error("❌ 日次更新バッチでエラーが発生")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"❌ 予期しないエラー: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
