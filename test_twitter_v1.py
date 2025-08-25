#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter API v1.1 テストスクリプト
OAuth 1.0a認証のみを使用
"""

import tweepy
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

def test_twitter_v1():
    """Twitter API v1.1接続テスト"""
    try:
        # OAuth 1.0a認証情報を取得
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        print(f"Consumer Key: {consumer_key[:10]}..." if consumer_key else "Consumer Key: 未設定")
        print(f"Access Token: {access_token[:10]}..." if access_token else "Access Token: 未設定")
        
        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            print("❌ OAuth 1.0a認証情報が不足しています")
            return False
        
        # OAuth 1.0a認証
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        # API v1.1クライアント作成
        api = tweepy.API(auth)
        
        # 接続テスト（ユーザー情報取得）
        user = api.verify_credentials()
        print(f"✅ OAuth 1.0a認証成功: @{user.screen_name}")
        
        # テストツイート投稿
        test_tweet = "🤖 大谷翔平成績データ Twitter自動投稿ボットのテスト投稿です #大谷翔平 #テスト"
        
        print(f"📝 テストツイート: {test_tweet}")
        response = input("このツイートを投稿しますか？ (y/n): ")
        
        if response.lower() == 'y':
            # ツイート投稿
            status = api.update_status(test_tweet)
            print(f"✅ ツイート投稿成功！")
            print(f"📱 ツイートID: {status.id}")
            print(f"🔗 URL: https://twitter.com/{user.screen_name}/status/{status.id}")
            return True
        else:
            print("❌ ツイート投稿をキャンセルしました")
            return False
            
    except Exception as e:
        print(f"❌ Twitter API v1.1接続エラー: {e}")
        return False

if __name__ == '__main__':
    print("🐦 Twitter API v1.1接続テスト")
    print("=" * 50)
    
    success = test_twitter_v1()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Twitter API v1.1接続・投稿テスト成功！")
    else:
        print("❌ Twitter API v1.1接続・投稿テスト失敗")
