# -*- coding: utf-8 -*-
import pandas as pd
import json
from datetime import datetime, timedelta

def create_home_run_prediction():
    """2025年の残り試合でのホームラン予測を生成"""
    
    # 2024年のデータを読み込み
    df_2024 = pd.read_csv('data/raw/ohtani_batting_gamelogs_2024.csv')
    df_2024['date'] = pd.to_datetime(df_2024['date'])
    
    # 2025年のデータを読み込み
    df_2025 = pd.read_csv('data/raw/ohtani_batting_api_2025.csv')
    df_2025['game_date'] = pd.to_datetime(df_2025['game_date'])
    
    # ドジャースの試合数を取得
    with open('data/processed/dodgers_games_2025.json', 'r', encoding='utf-8') as f:
        dodgers_data = json.load(f)
    
    total_games = dodgers_data['total_games']
    completed_games = dodgers_data['completed_games']
    remaining_games = dodgers_data['remaining_games']
    
    # 2024年の週次ホームラン率を計算
    import ast
    df_2024['stat_dict'] = df_2024['stat'].apply(ast.literal_eval)
    df_2024['home_runs'] = df_2024['stat_dict'].apply(lambda x: x.get('homeRuns', 0))
    df_2024['week_number'] = ((df_2024['date'] - df_2024['date'].min()).dt.days // 7) + 1
    weekly_2024 = df_2024.groupby('week_number')['home_runs'].sum().reset_index()
    
    # 2025年の現在の週次ホームラン率を計算
    df_2025['week_number'] = ((df_2025['game_date'] - df_2025['game_date'].min()).dt.days // 7) + 1
    weekly_2025 = df_2025.groupby('week_number')['home_runs'].sum().reset_index()
    
    # 2024年の平均週次ホームラン数を計算
    avg_weekly_hr_2024 = weekly_2024['home_runs'].mean()
    
    # 2025年の平均週次ホームラン数を計算
    avg_weekly_hr_2025 = weekly_2025['home_runs'].mean()
    
    # 予測に使用する週次ホームラン率（2025年の実績を重視）
    prediction_rate = (avg_weekly_hr_2025 * 0.7) + (avg_weekly_hr_2024 * 0.3)
    
    # 残り週数を計算
    remaining_weeks = remaining_games // 7 + (1 if remaining_games % 7 > 0 else 0)
    
    # 現在の週番号を取得
    current_week = weekly_2025['week_number'].max()
    
    # 予測データを生成
    prediction_data = []
    cumulative_home_runs = df_2025['home_runs'].sum()  # 現在の累積ホームラン数
    
    for week in range(current_week + 1, current_week + remaining_weeks + 1):
        # 週次ホームラン数を予測（ランダム性を加味）
        import random
        weekly_prediction = max(0, round(prediction_rate + random.uniform(-0.5, 0.5)))
        cumulative_home_runs += weekly_prediction
        
        prediction_data.append({
            'week': int(week),
            'weekly_home_runs': int(weekly_prediction),
            'cumulative_home_runs': int(cumulative_home_runs),
            'is_prediction': True
        })
    
    # 予測データを保存
    prediction_result = {
        'current_week': int(current_week),
        'remaining_weeks': int(remaining_weeks),
        'remaining_games': remaining_games,  # 残り試合数を追加
        'prediction_rate': round(prediction_rate, 2),
        'current_home_runs': int(df_2025['home_runs'].sum()),
        'predicted_total': int(cumulative_home_runs),
        'prediction_data': prediction_data
    }
    
    with open('data/processed/home_run_prediction_2025.json', 'w', encoding='utf-8') as f:
        json.dump(prediction_result, f, ensure_ascii=False, indent=2)
    
    print(f"📊 ホームラン予測データ生成完了:")
    print(f"現在の週: {current_week}週")
    print(f"残り週数: {remaining_weeks}週")
    print(f"予測週次ホームラン率: {prediction_rate:.2f}")
    print(f"現在のホームラン数: {df_2025['home_runs'].sum()}本")
    print(f"予測最終ホームラン数: {cumulative_home_runs}本")
    print(f"予測追加ホームラン数: {cumulative_home_runs - df_2025['home_runs'].sum()}本")
    
    return prediction_result

if __name__ == "__main__":
    import os
    os.makedirs('data/processed', exist_ok=True)
    
    print("🏟️ 2025年ホームラン予測データ生成ツール")
    print("=" * 50)
    
    prediction_data = create_home_run_prediction()
    
    print(f"\n✅ 予測データを保存しました: data/processed/home_run_prediction_2025.json")
