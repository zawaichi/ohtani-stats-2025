# 大谷翔平成績データ 2025

大谷翔平の2025年シーズンの成績データを表示するWebアプリケーション

## 🌟 特徴

- **リアルタイムデータ**: MLB.com APIから最新データを取得
- **比較表示**: 2024年と2025年の成績を比較
- **ホームラン予測**: 2024年データを基にした2025年予測
- **自動更新**: 毎日14時にデータを自動更新
- **レスポンシブデザイン**: PC・スマホ対応

## 📊 表示データ

### 投手成績
- 試合数、勝利、敗戦、防御率、奪三振など

### 打撃成績  
- 試合数、打率、本塁打、打点、盗塁など

### ホームラン推移
- 週次ベースの累積ホームラン数比較
- 2025年の残り期間予測

## 🚀 デプロイ方法

### Herokuでの公開

1. **Herokuアカウント作成**
   ```bash
   # Heroku CLIインストール
   brew install heroku/brew/heroku
   ```

2. **ログイン**
   ```bash
   heroku login
   ```

3. **アプリケーション作成**
   ```bash
   heroku create ohtani-stats-2025
   ```

4. **デプロイ**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **アプリケーション起動**
   ```bash
   heroku open
   ```

### ローカル実行

1. **依存関係インストール**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **アプリケーション起動**
   ```bash
   python3 test_app.py
   ```

3. **ブラウザでアクセス**
   ```
   http://localhost:8080
   ```

## 📁 プロジェクト構造

```
ohtani-stats-2025/
├── test_app.py                 # メインFlaskアプリケーション
├── daily_update_batch.py       # 日次更新バッチ
├── setup_scheduler.py          # スケジューラー設定
├── fetch_dodgers_games.py      # ドジャース試合データ取得
├── create_home_run_*.py        # ホームラン関連データ生成
├── data/                       # データディレクトリ
│   ├── raw/                    # 生データ
│   └── processed/              # 処理済みデータ
├── logs/                       # ログファイル
├── requirements.txt            # Python依存関係
├── Procfile                    # Heroku設定
└── runtime.txt                 # Pythonバージョン指定
```

## 🔧 設定

### 自動更新スケジュール
- **実行時間**: 毎日14:00 (日本時間)
- **設定方法**: `python3 setup_scheduler.py setup`
- **確認方法**: `python3 setup_scheduler.py check`

### 手動更新
```bash
# バッチ処理テスト
python3 test_batch.py

# 手動実行
python3 daily_update_batch.py
```

## 📱 アクセス方法

### ローカル
- **URL**: http://localhost:8080
- **スマホ**: http://[PCのIPアドレス]:8080

### 公開後
- **URL**: https://ohtani-stats-2025.herokuapp.com (例)

## 🛠️ 技術スタック

- **Backend**: Python 3.11, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Plotly.js
- **データ処理**: Pandas, NumPy
- **API**: MLB.com Stats API
- **デプロイ**: Heroku, Gunicorn

## 📈 データソース

- **MLB.com Stats API**: 公式統計データ
- **更新頻度**: 毎日14:00 (日本時間)
- **データ期間**: 2024年〜2025年

## 🤝 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

問題や質問がある場合は、GitHubのIssuesページでお知らせください。
