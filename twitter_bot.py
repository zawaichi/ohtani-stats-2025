#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大谷翔平成績データ Twitter自動投稿ボット
無料プランで月500ツイートまで投稿可能
"""

import tweepy
import json
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/twitter_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class OhtaniTwitterBot:
    def __init__(self):
        """Twitter API初期化"""
        self.api = None
        self.setup_twitter_api()
    
    def setup_twitter_api(self):
        """Twitter API設定"""
        try:
            # 環境変数から認証情報を取得
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if not bearer_token:
                logging.warning("Twitter Bearer Tokenが設定されていません")
                return
            
            # API v2クライアント（OAuth 2.0）
            self.client = tweepy.Client(bearer_token=bearer_token)
            logging.info("Twitter API v2 (OAuth 2.0) 認証成功")
            
        except Exception as e:
            logging.error(f"Twitter API認証エラー: {e}")
    
    def load_latest_stats(self):
        """最新の成績データを読み込み"""
        try:
            # 2024年データ
            with open('data/processed/ohtani_batting_2024_final.csv', 'r', encoding='utf-8') as f:
                import csv
                reader = csv.DictReader(f)
                batting_2024 = next(reader)
            
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
                'batting_average_2024': batting_2024.get('batting_average', 'N/A'),
                'home_runs_2024': batting_2024.get('home_runs', 0),
                'current_home_runs': prediction_data.get('current_home_runs', 0),
                'predicted_total': prediction_data.get('predicted_total', 0),
                'prediction_rate': prediction_data.get('prediction_rate', 0)
            }
            
            return stats
            
        except Exception as e:
            logging.error(f"データ読み込みエラー: {e}")
            return None
    
    def create_daily_tweet(self):
        """日次投稿用ツイート作成"""
        try:
            stats = self.load_latest_stats()
            if not stats:
                return None
            
            # 進捗率計算
            progress_rate = (stats.get('games_played', 0) / stats.get('total_games', 162)) * 100
            
            # ツイート内容作成
            tweet_text = f"""⚾ 大谷翔平 2025年シーズン成績更新

🏟️ 試合進捗: {stats.get('games_played', 0)}/{stats.get('total_games', 162)}試合 ({progress_rate:.1f}%)
🏃 本塁打: {stats.get('current_home_runs', 0)}本 (2024年: {stats.get('home_runs_2024', 0)}本)
💪 打率: {stats.get('batting_average_2024', 'N/A')} (2024年実績)

📊 予測最終本塁打: {stats.get('predicted_total', 0)}本
📈 残り試合: {stats.get('remaining_games', 0)}試合

#大谷翔平 #ドジャース #MLB #野球"""
            
            return tweet_text
            
        except Exception as e:
            logging.error(f"ツイート作成エラー: {e}")
            return None
    
    def create_home_run_tweet(self, home_runs):
        """ホームラン達成時のツイート"""
        tweet_text = f"""🎉 大谷翔平 ホームラン達成！

🏃 {home_runs}号本塁打を放ちました！

⚾ 2025年シーズン通算{home_runs}本目
📊 予測達成率: {self.calculate_prediction_rate(home_runs)}%

#大谷翔平 #ホームラン #ドジャース #MLB #野球"""
        
        return tweet_text
    
    def calculate_prediction_rate(self, current_home_runs):
        """予測達成率を計算"""
        try:
            with open('data/processed/home_run_prediction_2025.json', 'r', encoding='utf-8') as f:
                prediction = json.load(f)
            
            predicted_total = prediction.get('predicted_total', 55)
            rate = (current_home_runs / predicted_total) * 100
            return round(rate, 1)
            
        except:
            return 0
    
    def post_tweet(self, tweet_text):
        """ツイート投稿"""
        try:
            if not self.client:
                logging.error("Twitter APIクライアントが初期化されていません")
                return False
            
            # OAuth 2.0では投稿に追加の認証が必要
            # 一時的にOAuth 1.0aの認証情報も使用
            consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
            consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            
            if all([consumer_key, consumer_secret, access_token, access_token_secret]):
                # OAuth 1.0a認証で投稿用クライアントを作成
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)
                
                # ツイート投稿
                api.update_status(tweet_text)
                logging.info(f"ツイート投稿成功: {tweet_text[:50]}...")
                return True
            else:
                logging.error("OAuth 1.0a認証情報が不足しています")
                return False
                
        except Exception as e:
            logging.error(f"ツイート投稿エラー: {e}")
            return False
    
    def daily_update(self):
        """日次更新投稿"""
        tweet_text = self.create_daily_tweet()
        if tweet_text:
            return self.post_tweet(tweet_text)
        return False

def main():
    """メイン処理"""
    bot = OhtaniTwitterBot()
    
    # 日次更新投稿
    success = bot.daily_update()
    
    if success:
        logging.info("日次Twitter投稿完了")
    else:
        logging.error("日次Twitter投稿失敗")

if __name__ == '__main__':
    main()
