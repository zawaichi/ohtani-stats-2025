#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter API設定ガイド
大谷翔平成績データの自動投稿用
"""

import os

def create_env_template():
    """環境変数テンプレートファイルを作成"""
    env_content = """# Twitter API認証情報
# developer.twitter.com で取得した認証情報を設定してください

# Consumer Keys (API Key)
TWITTER_CONSUMER_KEY=your_consumer_key_here

# Consumer Secret (API Secret)
TWITTER_CONSUMER_SECRET=your_consumer_secret_here

# Access Token
TWITTER_ACCESS_TOKEN=your_access_token_here

# Access Token Secret
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here

# 投稿設定
TWITTER_ENABLED=true
TWITTER_DAILY_UPDATE=true
TWITTER_HOME_RUN_ALERT=true
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .envファイルを作成しました")
    print("📝 認証情報を設定してください")

def show_setup_instructions():
    """設定手順を表示"""
    instructions = """
🐦 Twitter API設定手順

1️⃣ Twitter Developer Account作成
   - https://developer.twitter.com にアクセス
   - 「Apply for a developer account」をクリック
   - Basicプラン（無料）を選択
   - アプリケーション情報を入力

2️⃣ アプリケーション作成
   - 「Create App」をクリック
   - アプリ名: 「Ohtani Stats Bot」
   - 説明: 「大谷翔平成績データ自動投稿ボット」

3️⃣ 認証情報取得
   - 「Keys and tokens」タブを開く
   - 「Consumer Keys」をコピー
   - 「Access Token and Secret」を生成・コピー

4️⃣ 環境変数設定
   - .envファイルに認証情報を設定
   - 例: TWITTER_CONSUMER_KEY=abc123...

5️⃣ 権限設定
   - 「App permissions」で「Read and Write」を選択
   - 変更を保存

6️⃣ テスト実行
   python3 test_twitter.py

📊 投稿内容例:
   - 日次成績更新
   - ホームラン達成通知
   - 予測達成率更新

💰 コスト: 完全無料（月500ツイートまで）
"""
    
    print(instructions)

def main():
    """メイン処理"""
    print("🐦 大谷翔平成績データ Twitter自動投稿設定")
    print("=" * 50)
    
    # 環境変数テンプレート作成
    create_env_template()
    
    # 設定手順表示
    show_setup_instructions()
    
    print("\n🎯 次のステップ:")
    print("1. Twitter Developer Account作成")
    print("2. 認証情報を.envファイルに設定")
    print("3. python3 test_twitter.py でテスト")
    print("4. 成功したら自動投稿開始！")

if __name__ == '__main__':
    main()
