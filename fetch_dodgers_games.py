# -*- coding: utf-8 -*-
import requests
import pandas as pd
from datetime import datetime
import json

def fetch_dodgers_games_2025():
    """ドジャースの2025年シーズンの試合数を取得"""
    
    # MLB Stats APIを使用してドジャースの試合データを取得
    # ドジャースのチームID: 119 (Los Angeles Dodgers)
    team_id = 119
    season = 2025
    
    try:
        # ドジャースの試合スケジュールを取得
        url = f"https://statsapi.mlb.com/api/v1/schedule"
        params = {
            'sportId': 1,  # MLB
            'teamId': team_id,
            'season': season,
            'gameType': 'R',  # Regular Season
            'fields': 'dates,games,gamePk,gameDate,status,abstractGameState'
        }
        
        print(f"ドジャースの2025年シーズンデータを取得中...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # 試合データを解析
        total_games = 0
        completed_games = 0
        today = datetime.now().strftime('%Y-%m-%d')
        
        if 'dates' in data:
            for date_info in data['dates']:
                for game in date_info.get('games', []):
                    total_games += 1
                    game_date = game.get('gameDate', '')[:10]  # YYYY-MM-DD形式
                    game_status = game.get('status', {}).get('abstractGameState', '')
                    
                    # 完了した試合をカウント
                    if game_status == 'Final':
                        completed_games += 1
                        print(f"完了試合: {game_date} - {game_status}")
        
        # 結果を表示
        print(f"\n📊 ドジャース2025年シーズン試合状況:")
        print(f"総試合数: {total_games}試合")
        print(f"完了試合数: {completed_games}試合")
        print(f"残り試合数: {total_games - completed_games}試合")
        print(f"進捗率: {round(completed_games/total_games*100, 1)}%")
        
        # データを保存
        dodgers_data = {
            'team': 'Los Angeles Dodgers',
            'season': season,
            'total_games': total_games,
            'completed_games': completed_games,
            'remaining_games': total_games - completed_games,
            'progress_percentage': round(completed_games/total_games*100, 1),
            'last_updated': today
        }
        
        with open('data/processed/dodgers_games_2025.json', 'w', encoding='utf-8') as f:
            json.dump(dodgers_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ ドジャース試合データを保存しました: data/processed/dodgers_games_2025.json")
        
        return dodgers_data
        
    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None

def get_dodgers_games_fallback():
    """フォールバック用のドジャース試合データ（手動設定）"""
    # 2025年8月20日時点での推定値
    return {
        'team': 'Los Angeles Dodgers',
        'season': 2025,
        'total_games': 162,
        'completed_games': 124,  # 推定値
        'remaining_games': 38,
        'progress_percentage': 76.5,
        'last_updated': '2025-08-20'
    }

if __name__ == "__main__":
    # データディレクトリが存在しない場合は作成
    import os
    os.makedirs('data/processed', exist_ok=True)
    
    print("🏟️ ドジャース2025年シーズン試合数取得ツール")
    print("=" * 50)
    
    # APIからデータを取得
    dodgers_data = fetch_dodgers_games_2025()
    
    if not dodgers_data:
        print("\n⚠️ APIからの取得に失敗しました。フォールバックデータを使用します。")
        dodgers_data = get_dodgers_games_fallback()
        
        # フォールバックデータも保存
        with open('data/processed/dodgers_games_2025.json', 'w', encoding='utf-8') as f:
            json.dump(dodgers_data, f, ensure_ascii=False, indent=2)
        
        print(f"📊 フォールバックデータ:")
        print(f"完了試合数: {dodgers_data['completed_games']}試合")
        print(f"残り試合数: {dodgers_data['remaining_games']}試合")
        print(f"進捗率: {dodgers_data['progress_percentage']}%")
    
    print(f"\n🎯 最終結果:")
    print(f"ドジャース {dodgers_data['completed_games']}試合完了 / {dodgers_data['total_games']}試合")
    print(f"残り{dodgers_data['remaining_games']}試合（{dodgers_data['progress_percentage']}%進行）")
