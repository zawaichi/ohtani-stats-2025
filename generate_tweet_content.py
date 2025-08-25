#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手動投稿用ツイート内容生成スクリプト
大谷翔平成績データのツイート内容を生成
"""

import json
import csv
from datetime import datetime

def load_latest_stats():
    """最新の成績データを読み込み"""
    try:
        # 2024年データ
        with open('data/processed/ohtani_batting_2024_final.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batting_2024 = next(reader)
        
        # 2025年データ（最新の打率を取得）
        current_batting_avg_2025 = 'N/A'
        try:
            with open('data/raw/ohtani_batting_api_2025.csv', 'r', encoding='utf-8') as f:
                reader_2025 = csv.DictReader(f)
                rows_2025 = list(reader_2025)
                if rows_2025:
                    # 最新の行の打率を取得
                    current_batting_avg_2025 = rows_2025[-1].get('avg', 'N/A')
        except Exception as e:
            print(f"2025年データ読み込みエラー: {e}")
        
        # ホームラン予測データ
        with open('data/processed/home_run_prediction_2025.json', 'r', encoding='utf-8') as f:
            prediction_data = json.load(f)
        
        # ドジャース試合データ
        with open('data/processed/dodgers_games_2025.json', 'r', encoding='utf-8') as f:
            dodgers_data = json.load(f)
        
        # 統合データ
        stats = {
            'games_played': dodgers_data.get('completed_games', 0),
            'total_games': dodgers_data.get('total_games', 162),
            'remaining_games': dodgers_data.get('remaining_games', 0),
            'batting_average_2025': current_batting_avg_2025,
            'batting_average_2024': batting_2024.get('avg', 'N/A'),
            'home_runs_2024': batting_2024.get('home_runs', 0),
            'current_home_runs': prediction_data.get('current_home_runs', 0),
            'predicted_total': prediction_data.get('predicted_total', 0),
            'prediction_rate': prediction_data.get('prediction_rate', 0)
        }
        
        return stats
        
    except Exception as e:
        print(f"データ読み込みエラー: {e}")
        return None

def create_daily_tweet():
    """日次投稿用ツイート作成"""
    try:
        stats = load_latest_stats()
        if not stats:
            return None
        
        # 進捗率計算
        progress_rate = (stats.get('games_played', 0) / stats.get('total_games', 162)) * 100
        
        # 打率の表示形式を調整（10倍して表示）
        batting_avg_2025 = stats.get('batting_average_2025', 'N/A')
        batting_avg_2024 = stats.get('batting_average_2024', 'N/A')
        
        if batting_avg_2025 != 'N/A':
            try:
                batting_avg_2025 = float(batting_avg_2025) * 10
                batting_avg_2025 = f"{batting_avg_2025:.2f}"
            except:
                batting_avg_2025 = 'N/A'
        
        if batting_avg_2024 != 'N/A':
            try:
                batting_avg_2024 = float(batting_avg_2024) * 10
                batting_avg_2024 = f"{batting_avg_2024:.2f}"
            except:
                batting_avg_2024 = 'N/A'
        
        # ツイート内容作成
        tweet_text = f"""⚾ 大谷翔平 2025年シーズン成績更新

🏟️ 試合進捗: {stats.get('games_played', 0)}/{stats.get('total_games', 162)}試合 ({progress_rate:.1f}%)
🏃 本塁打: {stats.get('current_home_runs', 0)}本 (2024年: {stats.get('home_runs_2024', 0)}本)
💪 打率: {batting_avg_2025} (2024年: {batting_avg_2024})

📊 予測最終本塁打: {stats.get('predicted_total', 0)}本
📈 残り試合: {stats.get('remaining_games', 0)}試合

#大谷翔平 #ドジャース #MLB #野球"""
        
        return tweet_text
        
    except Exception as e:
        print(f"ツイート作成エラー: {e}")
        return None

def create_home_run_tweet(home_runs):
    """ホームラン達成時のツイート"""
    try:
        with open('data/processed/home_run_prediction_2025.json', 'r', encoding='utf-8') as f:
            prediction = json.load(f)
        
        predicted_total = prediction.get('predicted_total', 55)
        rate = (home_runs / predicted_total) * 100
        
        tweet_text = f"""🎉 大谷翔平 ホームラン達成！

🏃 {home_runs}号本塁打を放ちました！

⚾ 2025年シーズン通算{home_runs}本目
📊 予測達成率: {rate:.1f}%

#大谷翔平 #ホームラン #ドジャース #MLB #野球"""
        
        return tweet_text
        
    except Exception as e:
        print(f"ホームランツイート作成エラー: {e}")
        return None

def main():
    """メイン処理"""
    print("🐦 大谷翔平成績データ ツイート内容生成")
    print("=" * 60)
    
    # 日次更新ツイート
    daily_tweet = create_daily_tweet()
    if daily_tweet:
        print("📝 【日次更新ツイート】")
        print("-" * 40)
        print(daily_tweet)
        print("-" * 40)
        print(f"文字数: {len(daily_tweet)}文字")
        print()
    
    # ホームラン達成ツイート（例：30号達成時）
    home_run_tweet = create_home_run_tweet(30)
    if home_run_tweet:
        print("🎉 【ホームラン達成ツイート（30号例）】")
        print("-" * 40)
        print(home_run_tweet)
        print("-" * 40)
        print(f"文字数: {len(home_run_tweet)}文字")
        print()
    
    print("✅ ツイート内容生成完了！")
    print("📱 上記の内容をコピーして手動で投稿してください")

if __name__ == '__main__':
    main()
