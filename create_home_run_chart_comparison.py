# -*- coding: utf-8 -*-
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import ast

def create_home_run_progression_by_week():
    """週番号ベースで2024年と2025年のホームラン累積推移データを作成"""
    
    # 2024年のデータを処理
    df_2024 = pd.read_csv('data/raw/ohtani_batting_gamelogs_2024.csv')
    df_2024['date'] = pd.to_datetime(df_2024['date'])
    
    # stat列からホームラン数を抽出
    home_runs_2024 = []
    for stat_str in df_2024['stat']:
        try:
            stat_dict = ast.literal_eval(stat_str)
            home_runs_2024.append(stat_dict.get('homeRuns', 0))
        except:
            home_runs_2024.append(0)
    
    df_2024['home_runs'] = home_runs_2024
    df_2024['cumulative_home_runs'] = df_2024['home_runs'].cumsum()
    
    # 週番号を計算（シーズン開始からの週数）
    df_2024['week_number'] = ((df_2024['date'] - df_2024['date'].min()).dt.days // 7) + 1
    
    # 週ごとにグループ化して累積ホームラン数を取得
    weekly_2024 = df_2024.groupby('week_number')['cumulative_home_runs'].max().reset_index()
    
    # 2025年のデータを処理
    df_2025 = pd.read_csv('data/raw/ohtani_batting_api_2025.csv')
    df_2025['game_date'] = pd.to_datetime(df_2025['game_date'])
    df_2025['home_runs'] = pd.to_numeric(df_2025['home_runs'], errors='coerce').fillna(0)
    df_2025['cumulative_home_runs'] = df_2025['home_runs'].cumsum()
    
    # 週番号を計算（シーズン開始からの週数）
    df_2025['week_number'] = ((df_2025['game_date'] - df_2025['game_date'].min()).dt.days // 7) + 1
    
    # 週ごとにグループ化して累積ホームラン数を取得
    weekly_2025 = df_2025.groupby('week_number')['cumulative_home_runs'].max().reset_index()
    
    # 全週番号の範囲を取得（2024年と2025年の最大週数）
    max_weeks = max(weekly_2024['week_number'].max(), weekly_2025['week_number'].max())
    all_weeks = list(range(1, max_weeks + 1))
    
    # 週番号ごとのデータを辞書に変換
    week_data = {}
    for week in all_weeks:
        week_data[week] = {
            '2024': weekly_2024[weekly_2024['week_number'] == week]['cumulative_home_runs'].iloc[0] if week in weekly_2024['week_number'].values else None,
            '2025': weekly_2025[weekly_2025['week_number'] == week]['cumulative_home_runs'].iloc[0] if week in weekly_2025['week_number'].values else None
        }
    
    # CSV形式のデータを作成
    csv_data = []
    for week in all_weeks:
        csv_data.append({
            '週': week,
            '2024年': int(week_data[week]['2024']) if week_data[week]['2024'] is not None else '',
            '2025年': int(week_data[week]['2025']) if week_data[week]['2025'] is not None else ''
        })
    
    # チャート用のデータ形式も作成
    chart_data = {
        'weeks': all_weeks,
        '2024': [int(week_data[week]['2024']) if week_data[week]['2024'] is not None else None for week in all_weeks],
        '2025': [int(week_data[week]['2025']) if week_data[week]['2025'] is not None else None for week in all_weeks]
    }
    
    return csv_data, chart_data

def create_comparison_chart_html(csv_data, chart_data):
    """週番号ベースの比較折れ線グラフのHTMLを生成"""
    
    # CSVデータを表示用のテーブルに変換
    table_html = ""
    for row in csv_data:
        week = row['週']
        hr_2024 = row['2024年'] if row['2024年'] != '' else '-'
        hr_2025 = row['2025年'] if row['2025年'] != '' else '-'
        table_html += f"<tr><td>{week}</td><td>{hr_2024}</td><td>{hr_2025}</td></tr>"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>大谷翔平 ホームラン累積推移比較 - 2024年 vs 2025年（週番号ベース）</title>
        <meta charset="utf-8">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f8f9fa;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                padding: 25px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #2c3e50;
                margin-bottom: 10px;
            }}
            .chart-container {{
                margin-top: 20px;
            }}
            .data-table {{
                margin-top: 30px;
                overflow-x: auto;
            }}
            .data-table table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            .data-table th, .data-table td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }}
            .data-table th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            .data-table tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .stats-summary {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
            }}
            .stat-item {{
                text-align: center;
            }}
            .stat-value {{
                font-size: 24px;
                font-weight: bold;
            }}
            .stat-value.2024 {{
                color: #95a5a6;
            }}
            .stat-value.2025 {{
                color: #e74c3c;
            }}
            .stat-label {{
                font-size: 14px;
                color: #7f8c8d;
                margin-top: 5px;
            }}
            .nav-links {{
                text-align: center;
                margin: 20px 0;
            }}
            .nav-links a {{
                display: inline-block;
                margin: 0 10px;
                padding: 10px 20px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }}
            .nav-links a:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏟️ 大谷翔平 ホームラン累積推移比較</h1>
                <p>2024年 vs 2025年 週番号ベース累積ホームラン数の推移</p>
            </div>
            
            <div class="nav-links">
                <a href="/">📊 成績データ</a>
                <a href="/home-run-chart">📈 ホームラン推移</a>
                <a href="/home-run-comparison">📊 ホームラン比較</a>
            </div>
            
            <div class="chart-container" id="chart"></div>
            
            <div class="data-table">
                <h3>週別累積ホームラン数データ</h3>
                <table>
                    <thead>
                        <tr>
                            <th>週</th>
                            <th>2024年</th>
                            <th>2025年</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_html}
                    </tbody>
                </table>
            </div>
            
            <div class="stats-summary">
                <div class="stat-item">
                    <div class="stat-value 2024">{max([row['2024年'] for row in csv_data if row['2024年'] != ''])}</div>
                    <div class="stat-label">2024年最終累積</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value 2025">{max([row['2025年'] for row in csv_data if row['2025年'] != ''])}</div>
                    <div class="stat-label">2025年現在累積</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{len([row for row in csv_data if row['2024年'] != ''])}</div>
                    <div class="stat-label">2024年データ週数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{len([row for row in csv_data if row['2025年'] != ''])}</div>
                    <div class="stat-label">2025年データ週数</div>
                </div>
            </div>
        </div>
        
        <script>
            const chartData = {json.dumps(chart_data)};
            
            const trace2024 = {{
                x: chartData.weeks,
                y: chartData['2024'].map(val => val === null ? null : val),
                type: 'scatter',
                mode: 'lines+markers',
                line: {{
                    color: '#95a5a6',
                    width: 2,
                    dash: 'dash'
                }},
                marker: {{
                    color: '#95a5a6',
                    size: 6
                }},
                name: '2024年'
            }};
            
            const trace2025 = {{
                x: chartData.weeks,
                y: chartData['2025'].map(val => val === null ? null : val),
                type: 'scatter',
                mode: 'lines+markers',
                line: {{
                    color: '#e74c3c',
                    width: 3
                }},
                marker: {{
                    color: '#e74c3c',
                    size: 8
                }},
                name: '2025年'
            }};
            
            const layout = {{
                title: {{
                    text: 'ホームラン累積推移比較 - 2024年 vs 2025年（週番号ベース）',
                    font: {{
                        size: 18,
                        color: '#2c3e50'
                    }}
                }},
                xaxis: {{
                    title: 'シーズン開始からの週数',
                    rangemode: 'tozero'
                }},
                yaxis: {{
                    title: '累積ホームラン数',
                    rangemode: 'tozero'
                }},
                plot_bgcolor: 'white',
                paper_bgcolor: 'white',
                margin: {{
                    l: 60,
                    r: 40,
                    t: 80,
                    b: 80
                }},
                showlegend: true,
                legend: {{
                    x: 0.02,
                    y: 0.98,
                    bgcolor: 'rgba(255,255,255,0.8)',
                    bordercolor: '#ccc',
                    borderwidth: 1
                }}
            }};
            
            const config = {{
                responsive: true,
                displayModeBar: false
            }};
            
            Plotly.newPlot('chart', [trace2024, trace2025], layout, config);
        </script>
    </body>
    </html>
    """
    
    # HTMLファイルとして保存
    with open('data/processed/home_run_week_comparison_chart.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("週番号ベースホームラン比較チャートのHTMLを生成しました: data/processed/home_run_week_comparison_chart.html")

def save_week_comparison_data(csv_data, chart_data):
    """週番号ベース比較データをJSONファイルとして保存"""
    
    # CSVデータも含めて保存
    data_to_save = {
        'csv_data': csv_data,
        'chart_data': chart_data
    }
    
    with open('data/processed/home_run_week_comparison_data.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    
    # CSVファイルも保存
    df_csv = pd.DataFrame(csv_data)
    df_csv.to_csv('data/processed/home_run_week_comparison.csv', index=False, encoding='utf-8')
    
    print("週番号ベースホームラン比較データを保存しました:")
    print("  - data/processed/home_run_week_comparison_data.json")
    print("  - data/processed/home_run_week_comparison.csv")

if __name__ == "__main__":
    # データディレクトリが存在しない場合は作成
    import os
    os.makedirs('data/processed', exist_ok=True)
    
    print("週番号ベースホームラン累積推移データを作成中...")
    csv_data, chart_data = create_home_run_progression_by_week()
    
    print(f"データ期間: 1週目から{len(csv_data)}週目まで")
    print(f"2024年最終累積ホームラン数: {max([row['2024年'] for row in csv_data if row['2024年'] != ''])}")
    print(f"2025年現在累積ホームラン数: {max([row['2025年'] for row in csv_data if row['2025年'] != ''])}")
    
    # サンプルデータを表示
    print("\n📊 サンプルデータ（最初の10週）:")
    print("週,2024年,2025年")
    for i, row in enumerate(csv_data[:10]):
        week = row['週']
        hr_2024 = row['2024年'] if row['2024年'] != '' else '-'
        hr_2025 = row['2025年'] if row['2025年'] != '' else '-'
        print(f"{week},{hr_2024},{hr_2025}")
    
    # 比較チャートHTMLを生成
    create_comparison_chart_html(csv_data, chart_data)
    
    # 比較データを保存
    save_week_comparison_data(csv_data, chart_data)
    
    print("\n✅ 週番号ベースホームラン累積推移比較チャートの作成が完了しました！")
    print("📊 チャートファイル: data/processed/home_run_week_comparison_chart.html")
    print("📈 データファイル: data/processed/home_run_week_comparison_data.json")
    print("📋 CSVファイル: data/processed/home_run_week_comparison.csv")
