# -*- coding: utf-8 -*-
"""
2024年大谷翔平データ取得スクリプト
MLB.comから2024年の投手・打撃成績を取得
"""

import requests
import pandas as pd
import json
from datetime import datetime
import os

class OhtaniDataFetcher2024:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"
        self.player_id = "660271"  # 大谷翔平のMLB ID
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def get_pitching_stats_2024(self):
        """2024年投手成績を取得"""
        try:
            # 2024年投手成績API
            url = f"{self.base_url}/people/{self.player_id}/stats"
            params = {
                'stats': 'pitching',
                'group': 'pitching',
                'season': '2024',
                'sportIds': '1'  # MLB
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'stats' in data and data['stats']:
                stats = data['stats'][0]['splits'][0]['stat']
                return {
                    'era': stats.get('era', 0.0),
                    'games': stats.get('gamesPlayed', 0),
                    'games_started': stats.get('gamesStarted', 0),
                    'wins': stats.get('wins', 0),
                    'losses': stats.get('losses', 0),
                    'strikeouts': stats.get('strikeOuts', 0),
                    'innings_pitched': stats.get('inningsPitched', 0.0),
                    'whip': stats.get('whip', 0.0),
                    'hits': stats.get('hits', 0),
                    'walks': stats.get('baseOnBalls', 0),
                    'home_runs_allowed': stats.get('homeRuns', 0),
                    'saves': stats.get('saves', 0),
                    'holds': stats.get('holds', 0)
                }
            else:
                print("2024年投手データが見つかりませんでした")
                return None
                
        except Exception as e:
            print(f"投手データ取得エラー: {e}")
            return None
    
    def get_batting_stats_2024(self):
        """2024年打撃成績を取得"""
        try:
            # 2024年打撃成績API
            url = f"{self.base_url}/people/{self.player_id}/stats"
            params = {
                'stats': 'batting',
                'group': 'hitting',
                'season': '2024',
                'sportIds': '1'  # MLB
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'stats' in data and data['stats']:
                stats = data['stats'][0]['splits'][0]['stat']
                return {
                    'avg': stats.get('avg', 0.0),
                    'games': stats.get('gamesPlayed', 0),
                    'at_bats': stats.get('atBats', 0),
                    'hits': stats.get('hits', 0),
                    'home_runs': stats.get('homeRuns', 0),
                    'rbi': stats.get('rbi', 0),
                    'runs': stats.get('runs', 0),
                    'stolen_bases': stats.get('stolenBases', 0),
                    'ops': stats.get('ops', 0.0),
                    'obp': stats.get('obp', 0.0),
                    'slg': stats.get('slg', 0.0),
                    'doubles': stats.get('doubles', 0),
                    'triples': stats.get('triples', 0),
                    'walks': stats.get('baseOnBalls', 0),
                    'strikeouts': stats.get('strikeOuts', 0)
                }
            else:
                print("2024年打撃データが見つかりませんでした")
                return None
                
        except Exception as e:
            print(f"打撃データ取得エラー: {e}")
            return None
    
    def get_game_logs_2024(self):
        """2024年ゲームログを取得"""
        try:
            # 投手ゲームログ
            pitching_url = f"{self.base_url}/people/{self.player_id}/stats"
            pitching_params = {
                'stats': 'gameLog',
                'group': 'pitching',
                'season': '2024',
                'sportIds': '1'
            }
            
            response = requests.get(pitching_url, headers=self.headers, params=pitching_params)
            response.raise_for_status()
            
            pitching_data = response.json()
            
            # 打撃ゲームログ
            batting_url = f"{self.base_url}/people/{self.player_id}/stats"
            batting_params = {
                'stats': 'gameLog',
                'group': 'hitting',
                'season': '2024',
                'sportIds': '1'
            }
            
            response = requests.get(batting_url, headers=self.headers, params=batting_params)
            response.raise_for_status()
            
            batting_data = response.json()
            
            return {
                'pitching_games': pitching_data.get('stats', []),
                'batting_games': batting_data.get('stats', [])
            }
            
        except Exception as e:
            print(f"ゲームログ取得エラー: {e}")
            return None
    
    def save_data_to_csv(self, pitching_stats, batting_stats, game_logs):
        """データをCSVファイルに保存"""
        try:
            # データディレクトリ作成
            os.makedirs('data/raw', exist_ok=True)
            
            # 投手成績保存
            if pitching_stats:
                df_pitching = pd.DataFrame([pitching_stats])
                df_pitching.to_csv('data/raw/ohtani_pitching_2024.csv', index=False, encoding='utf-8')
                print("✅ 2024年投手成績を保存しました: data/raw/ohtani_pitching_2024.csv")
            
            # 打撃成績保存
            if batting_stats:
                df_batting = pd.DataFrame([batting_stats])
                df_batting.to_csv('data/raw/ohtani_batting_2024.csv', index=False, encoding='utf-8')
                print("✅ 2024年打撃成績を保存しました: data/raw/ohtani_batting_2024.csv")
            
            # ゲームログ保存
            if game_logs and game_logs.get('pitching_games'):
                pitching_games = game_logs['pitching_games']
                if pitching_games:
                    df_pitching_logs = pd.DataFrame(pitching_games[0].get('splits', []))
                    df_pitching_logs.to_csv('data/raw/ohtani_pitching_gamelogs_2024.csv', index=False, encoding='utf-8')
                    print("✅ 2024年投手ゲームログを保存しました: data/raw/ohtani_pitching_gamelogs_2024.csv")
            
            if game_logs and game_logs.get('batting_games'):
                batting_games = game_logs['batting_games']
                if batting_games:
                    df_batting_logs = pd.DataFrame(batting_games[0].get('splits', []))
                    df_batting_logs.to_csv('data/raw/ohtani_batting_gamelogs_2024.csv', index=False, encoding='utf-8')
                    print("✅ 2024年打撃ゲームログを保存しました: data/raw/ohtani_batting_gamelogs_2024.csv")
                    
        except Exception as e:
            print(f"データ保存エラー: {e}")
    
    def fetch_all_2024_data(self):
        """2024年の全データを取得"""
        print("🔄 2024年大谷翔平データを取得中...")
        
        # 投手成績取得
        print("📊 投手成績を取得中...")
        pitching_stats = self.get_pitching_stats_2024()
        
        # 打撃成績取得
        print("🏏 打撃成績を取得中...")
        batting_stats = self.get_batting_stats_2024()
        
        # ゲームログ取得
        print("📈 ゲームログを取得中...")
        game_logs = self.get_game_logs_2024()
        
        # データ保存
        print("💾 データを保存中...")
        self.save_data_to_csv(pitching_stats, batting_stats, game_logs)
        
        # 結果表示
        print("\n📋 取得結果:")
        if pitching_stats:
            print(f"投手成績: ERA {pitching_stats['era']}, {pitching_stats['wins']}-{pitching_stats['losses']}, {pitching_stats['strikeouts']}奪三振")
        if batting_stats:
            print(f"打撃成績: 打率 {batting_stats['avg']}, {batting_stats['home_runs']}本塁打, {batting_stats['rbi']}打点")
        
        return {
            'pitching': pitching_stats,
            'batting': batting_stats,
            'game_logs': game_logs
        }

def main():
    """メイン実行関数"""
    fetcher = OhtaniDataFetcher2024()
    data = fetcher.fetch_all_2024_data()
    
    print("\n🎉 2024年データ取得完了！")
    print("データファイルは 'data/raw/' ディレクトリに保存されました。")

if __name__ == "__main__":
    main()
