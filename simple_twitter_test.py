#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
シンプルなTwitter APIテスト
"""

import tweepy
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

def test_twitter_connection():
    """Twitter API接続テスト"""
    try:
        # Bearer Tokenでテスト
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        print(f"Bearer Token: {bearer_token[:20]}..." if bearer_token else "Bearer Token: 未設定")
        
        if bearer_token:
            client = tweepy.Client(bearer_token=bearer_token)
            print("✅ Bearer Token認証成功")
            
            # 簡単なAPI呼び出しテスト
            try:
                # 自分のユーザー情報を取得
                me = client.get_me()
                print(f"✅ ユーザー情報取得成功: @{me.data.username}")
                return True
            except Exception as e:
                print(f"❌ API呼び出しエラー: {e}")
                return False
        else:
            print("❌ Bearer Tokenが設定されていません")
            return False
            
    except Exception as e:
        print(f"❌ 認証エラー: {e}")
        return False

def test_oauth1_connection():
    """OAuth 1.0a接続テスト"""
    try:
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        print(f"Consumer Key: {consumer_key[:10]}..." if consumer_key else "Consumer Key: 未設定")
        print(f"Access Token: {access_token[:10]}..." if access_token else "Access Token: 未設定")
        
        if all([consumer_key, consumer_secret, access_token, access_token_secret]):
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            
            # 接続テスト
            user = api.verify_credentials()
            print(f"✅ OAuth 1.0a認証成功: @{user.screen_name}")
            return True
        else:
            print("❌ OAuth 1.0a認証情報が不足しています")
            return False
            
    except Exception as e:
        print(f"❌ OAuth 1.0a認証エラー: {e}")
        return False

if __name__ == '__main__':
    print("🐦 Twitter API接続テスト")
    print("=" * 50)
    
    print("\n1️⃣ Bearer Token認証テスト")
    bearer_success = test_twitter_connection()
    
    print("\n2️⃣ OAuth 1.0a認証テスト")
    oauth_success = test_oauth1_connection()
    
    print("\n" + "=" * 50)
    if bearer_success or oauth_success:
        print("✅ いずれかの認証方法が成功しました！")
    else:
        print("❌ すべての認証方法が失敗しました")
        print("📝 新しいアプリケーションの作成を検討してください")
