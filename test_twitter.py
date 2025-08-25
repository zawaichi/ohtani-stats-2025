#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter API接続テスト
"""

import os
from dotenv import load_dotenv
import tweepy

def test_twitter_connection():
    """Twitter API接続テスト"""
    # 環境変数を読み込み
    load_dotenv()
    
    # 認証情報を取得
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("❌ 認証情報が設定されていません")
        print("📝 .envファイルを確認してください")
        return False
    
    try:
        # API認証
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        
        # 接続テスト
        user = api.verify_credentials()
        print(f"✅ Twitter API接続成功")
        print(f"👤 ユーザー: @{user.screen_name}")
        
        # テストツイート
        test_tweet = "🧪 大谷翔平成績データボット テスト投稿\n\n⚾ 自動投稿機能のテスト中です\n\n#大谷翔平 #テスト #MLB"
        
        # 投稿確認
        response = input("テストツイートを投稿しますか？ (y/n): ")
        if response.lower() == 'y':
            api.update_status(test_tweet)
            print("✅ テストツイート投稿成功")
        else:
            print("⏭️ テストツイートをスキップしました")
        
        return True
        
    except Exception as e:
        print(f"❌ Twitter API接続エラー: {e}")
        return False

if __name__ == '__main__':
    test_twitter_connection()
