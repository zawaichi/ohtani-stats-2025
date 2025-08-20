# -*- coding: utf-8 -*-
import pandas as pd
import json
import os

def create_home_run_with_prediction():
    """既存のホームラン比較データに2025年の予測データを統合"""
    
    # 既存の週次比較データを読み込み
    with open('data/processed/home_run_week_comparison_data.json', 'r', encoding='utf-8') as f:
        comparison_data = json.load(f)
    
    # 予測データを読み込み
    with open('data/processed/home_run_prediction_2025.json', 'r', encoding='utf-8') as f:
        prediction_data = json.load(f)
    
    # 既存の2025年データを取得
    chart_data = comparison_data['chart_data']
    csv_data = comparison_data['csv_data']
    
    # 予測データを2025年のデータに追加
    for pred in prediction_data['prediction_data']:
        week = pred['week']
        cumulative_hr = pred['cumulative_home_runs']
        
        # chart_dataに追加
        chart_data['2025'].append(cumulative_hr)
        chart_data['weeks'].append(week)
        
        # csv_dataに追加
        csv_data.append({
            '週': week,
            '2024年': None,  # 2024年は予測期間がないのでNone
            '2025年': cumulative_hr
        })
    
    # 統合データを保存
    integrated_data = {
        'chart_data': chart_data,
        'csv_data': csv_data,
        'prediction_info': {
            'current_week': prediction_data['current_week'],
            'remaining_weeks': prediction_data['remaining_weeks'],
            'remaining_games': prediction_data['remaining_games'],
            'prediction_rate': prediction_data['prediction_rate'],
            'current_home_runs': prediction_data['current_home_runs'],
            'predicted_total': prediction_data['predicted_total'],
            'additional_predicted': prediction_data['predicted_total'] - prediction_data['current_home_runs']
        }
    }
    
    with open('data/processed/home_run_with_prediction.json', 'w', encoding='utf-8') as f:
        json.dump(integrated_data, f, ensure_ascii=False, indent=2)
    
    # CSVファイルも更新
    df_csv = pd.DataFrame(csv_data)
    df_csv.to_csv('data/processed/home_run_with_prediction.csv', index=False, encoding='utf-8')
    
    print(f"📊 ホームラン予測統合データ生成完了:")
    print(f"現在の週: {prediction_data['current_week']}週")
    print(f"残り週数: {prediction_data['remaining_weeks']}週")
    print(f"現在のホームラン数: {prediction_data['current_home_runs']}本")
    print(f"予測最終ホームラン数: {prediction_data['predicted_total']}本")
    print(f"予測追加ホームラン数: {prediction_data['predicted_total'] - prediction_data['current_home_runs']}本")
    print(f"週次ホームラン率: {prediction_data['prediction_rate']:.2f}")
    
    return integrated_data

if __name__ == "__main__":
    os.makedirs('data/processed', exist_ok=True)
    
    print("🏟️ ホームラン予測統合データ生成ツール")
    print("=" * 50)
    
    integrated_data = create_home_run_with_prediction()
    
    print(f"\n✅ 統合データを保存しました:")
    print(f"  - data/processed/home_run_with_prediction.json")
    print(f"  - data/processed/home_run_with_prediction.csv")
