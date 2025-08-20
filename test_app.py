# -*- coding: utf-8 -*-
from flask import Flask, render_template_string
import pandas as pd
import json
import os

app = Flask(__name__)

def load_comparison_data():
    """比較データを読み込み"""
    try:
        # 2024年データ（参考用）
        df_batting_2024 = pd.read_csv('data/processed/ohtani_batting_2024_final.csv')
        batting_2024 = df_batting_2024.iloc[0].to_dict()
        
        # ドジャースの試合数を取得
        try:
            with open('data/processed/dodgers_games_2025.json', 'r', encoding='utf-8') as f:
                dodgers_data = json.load(f)
                games_played_2025 = dodgers_data['completed_games']
                remaining_games = dodgers_data['remaining_games']
                total_games = dodgers_data['total_games']
        except:
            # フォールバック値
            games_played_2025 = 126
            remaining_games = 36
            total_games = 162
        

        
        batting_2025 = {
            'avg': 0.285,
            'games': games_played_2025,
            'total_games': total_games,
            'home_runs': 44,
            'rbi': 82,
            'ops': 1.019,
            'stolen_bases': 15,
            'remaining_games': remaining_games
        }
        
        pitching_2025 = {
            'era': 3.47,
            'games': 9,
            'strikeouts': 32,
            'wins': 0,
            'losses': 0,
            'whip': 1.11,
            'innings_pitched': 23.1
        }
        
        return {
            'batting_2024': batting_2024,
            'batting_2025': batting_2025,
            'pitching_2025': pitching_2025
        }
    except Exception as e:
        print(f"データ読み込みエラー: {e}")
        # フォールバックデータ
        return {
            'batting_2024': {'avg': 0.31, 'games': 159, 'home_runs': 54, 'rbi': 130, 'ops': 1.066, 'stolen_bases': 59},
            'batting_2025': {'avg': 0.285, 'games': 126, 'total_games': 162, 'home_runs': 44, 'rbi': 82, 'ops': 1.019, 'stolen_bases': 15, 'remaining_games': 36},
            'pitching_2025': {'era': 3.47, 'games': 9, 'strikeouts': 32, 'wins': 0, 'losses': 0, 'whip': 1.11, 'innings_pitched': 23.1}
        }



def load_home_run_comparison_data():
    """ホームラン比較チャートデータを読み込み"""
    try:
        with open('data/processed/home_run_comparison_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ホームラン比較データ読み込みエラー: {e}")
        return None

def load_home_run_week_comparison_data():
    """週番号ベースホームラン比較チャートデータを読み込み（予測データ含む）"""
    try:
        with open('data/processed/home_run_with_prediction.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['chart_data']  # chart_dataの部分を返す
    except Exception as e:
        print(f"週番号ベースホームラン比較データ読み込みエラー: {e}")
        return None

def load_home_run_prediction_info():
    """ホームラン予測情報を読み込み"""
    try:
        with open('data/processed/home_run_with_prediction.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('prediction_info', {})
    except Exception as e:
        print(f"ホームラン予測情報読み込みエラー: {e}")
        return {}

@app.route('/')
def index():
    """2025年成績メインのページ"""
    data = load_comparison_data()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>大谷翔平成績データ - 2025年シーズン</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f8f9fa; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .header h1 {{ color: #2c3e50; margin-bottom: 10px; }}
            .header p {{ color: #7f8c8d; font-size: 16px; }}
            .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }}
            .stats-card {{ background: white; border-radius: 10px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .card-title {{ text-align: center; margin-bottom: 20px; font-size: 24px; font-weight: bold; color: #2c3e50; }}
            .stats-section {{ margin-bottom: 25px; }}
            .stats-section h3 {{ color: #34495e; margin-bottom: 15px; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px; }}
            .stats-row {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }}
            .stat-item {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
            .stat-value {{ font-size: 28px; font-weight: bold; margin-bottom: 5px; color: #2c3e50; }}
            .stat-label {{ font-size: 12px; color: #7f8c8d; text-transform: uppercase; margin-bottom: 5px; }}
            .stat-comparison {{ font-size: 11px; color: #95a5a6; font-style: italic; }}
            .highlight {{ background: linear-gradient(135deg, #3498db, #2980b9); color: white; }}
            .highlight .stat-value {{ color: white; }}
            .highlight .stat-label {{ color: rgba(255,255,255,0.8); }}
            .highlight .stat-comparison {{ color: rgba(255,255,255,0.7); }}
            .note {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin-top: 20px; }}
            .note h4 {{ color: #856404; margin: 0 0 10px 0; }}
            .note p {{ color: #856404; margin: 0; font-size: 14px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 14px; }}
            .season-badge {{ display: inline-block; padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; margin-left: 8px; background: #3498db; color: white; }}
            .nav-links {{ text-align: center; margin: 20px 0; display: flex; justify-content: center; gap: 10px; }}
            .nav-links a {{ display: inline-block; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; transition: background 0.3s; }}
            .nav-links a:hover {{ background: #2980b9; }}
            
            /* デバッグ用：スマホ表示の確認 */
            .stats-grid::before {{
                content: "PC表示";
                position: fixed;
                top: 10px;
                right: 10px;
                background: red;
                color: white;
                padding: 5px;
                z-index: 9999;
                font-size: 12px;
            }}
            
            /* スマホ表示用のスタイル */
            @media (max-width: 1200px) {{
                .stats-grid::before {{
                    content: "スマホ表示";
                    background: green;
                }}
                
                .stats-grid {{
                    grid-template-columns: 1fr !important;
                    gap: 30px !important;
                }}
                
                .stat-item {{
                    padding: 15px;
                    margin-bottom: 10px;
                }}
                
                .stat-value {{
                    font-size: 24px;
                }}
                
                .stat-label {{
                    font-size: 14px;
                }}
                
                .stat-comparison {{
                    font-size: 12px;
                }}
                
                .header h1 {{
                    font-size: 24px;
                }}
                
                .header p {{
                    font-size: 14px;
                }}
                
                .nav-links {{
                    flex-direction: column !important;
                    gap: 10px !important;
                }}
                
                .nav-links a {{
                    padding: 12px 20px;
                    font-size: 16px;
                }}
                
                .card-title {{
                    font-size: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
                    <div class="header">
            <h1>🏟️ 大谷翔平成績データ</h1>
            <p>2025年シーズン<span class="season-badge">手術後復帰</span></p>
            <p>現在進行中のシーズンの成績を表示しています</p>
            <p><strong>ドジャース {data['batting_2025']['games']}試合完了 / {data['batting_2025']['total_games']}試合</strong> 
               - 残り<span style="color: #e74c3c; font-weight: bold;">{data['batting_2025']['remaining_games']}試合</span>
               <span style="color: #7f8c8d; font-size: 14px;">（{round(data['batting_2025']['games']/data['batting_2025']['total_games']*100, 1)}%進行）</span></p>

        </div>
            
            <div class="nav-links">
                <a href="/">📊 成績データ</a>
                <a href="/home-run-comparison">📈 ホームラン推移</a>
            </div>
            
            <div class="stats-grid">
                <div class="stats-card">
                    <div class="card-title">⚾ 投手成績</div>
                    
                    <div class="stats-section">
                        <div class="stats-row">
                            <div class="stat-item">
                                <div class="stat-value">{data['pitching_2025']['era']}</div>
                                <div class="stat-label">ERA</div>
                                <div class="stat-comparison">(2024年: 登板なし)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['pitching_2025']['games']}</div>
                                <div class="stat-label">試合数</div>
                                <div class="stat-comparison">(2024年: 登板なし)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['pitching_2025']['strikeouts']}</div>
                                <div class="stat-label">奪三振</div>
                                <div class="stat-comparison">(2024年: 登板なし)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['pitching_2025']['wins']}-{data['pitching_2025']['losses']}</div>
                                <div class="stat-label">勝敗</div>
                                <div class="stat-comparison">(2024年: 登板なし)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['pitching_2025']['whip']}</div>
                                <div class="stat-label">WHIP</div>
                                <div class="stat-comparison">(2024年: 登板なし)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['pitching_2025']['innings_pitched']}</div>
                                <div class="stat-label">投球回</div>
                                <div class="stat-comparison">(2024年: 登板なし)</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="note">
                        <h4>📝 投手成績について</h4>
                        <p>2024年は肘の手術により投手としての登板はありませんでした。2025年は手術後の復帰シーズンとして、慎重に投球回数を管理しながら復調を目指しています。</p>
                    </div>
                </div>
                
                <div class="stats-card">
                    <div class="card-title">🏏 打撃成績</div>
                    
                    <div class="stats-section">
                        <div class="stats-row">
                            <div class="stat-item">
                                <div class="stat-value">{data['batting_2025']['avg'] * 10:.2f}</div>
                                <div class="stat-label">打率</div>
                                <div class="stat-comparison">(2024年: {data['batting_2024']['avg'] * 10:.2f})</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['batting_2025']['games']}</div>
                                <div class="stat-label">試合数</div>
                                <div class="stat-comparison">(2024年: {data['batting_2024']['games']}試合)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['batting_2025']['home_runs']}</div>
                                <div class="stat-label">本塁打</div>
                                <div class="stat-comparison">(2024年: {data['batting_2024']['home_runs']}本)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['batting_2025']['rbi']}</div>
                                <div class="stat-label">打点</div>
                                <div class="stat-comparison">(2024年: {data['batting_2024']['rbi']}打点)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['batting_2025']['ops']}</div>
                                <div class="stat-label">OPS</div>
                                <div class="stat-comparison">(2024年: {data['batting_2024']['ops']})</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{data['batting_2025']['stolen_bases']}</div>
                                <div class="stat-label">盗塁</div>
                                <div class="stat-comparison">(2024年: {data['batting_2024']['stolen_bases']}盗塁)</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="note">
                        <h4>🎯 打撃成績のポイント</h4>
                        <p>本塁打数は2024年と同数の44本を記録中。手術後も打撃面での復調は順調で、来シーズンの完全復活が期待されています。</p>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>データソース: <a href="https://www.mlb.com/player/shohei-ohtani-660271" target="_blank">MLB.com</a> | 最終更新: 2025年8月20日</p>
                <p>※2025年データは現在進行中のシーズンのため、最終的な成績とは異なる場合があります</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html



@app.route('/home-run-comparison')
def home_run_comparison():
    """ホームラン比較チャートページ（週番号ベース）"""
    week_comparison_data = load_home_run_week_comparison_data()
    prediction_info = load_home_run_prediction_info()
    
    if not week_comparison_data:
        return "ホームラン比較データが見つかりません。", 404
    
    chart_data_2024 = week_comparison_data['2024']
    chart_data_2025 = week_comparison_data['2025']
    weeks = week_comparison_data['weeks']
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>大谷翔平 ホームラン推移 - 2024年 vs 2025年（予測含む）</title>
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
                <h1>🏟️ 大谷翔平 ホームラン推移</h1>
                <p>2024年 vs 2025年 週番号ベース累積ホームラン数の推移（2025年は予測データ含む）</p>
            </div>
            
            <div class="nav-links">
                <a href="/">📊 成績データ</a>
                <a href="/home-run-comparison">📈 ホームラン推移</a>
            </div>
            
            <div class="chart-container" id="chart"></div>
            
            <div class="stats-summary">
                <div class="stat-item">
                    <div class="stat-value 2024">{max([x for x in chart_data_2024 if x is not None])}</div>
                    <div class="stat-label">2024年最終累積</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value 2025">{prediction_info.get('current_home_runs', max([x for x in chart_data_2025 if x is not None]))}</div>
                    <div class="stat-label">2025年現在累積</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{len([x for x in chart_data_2024 if x is not None])}</div>
                    <div class="stat-label">2024年データ週数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{prediction_info.get('current_week', len([x for x in chart_data_2025 if x is not None]))}</div>
                    <div class="stat-label">2025年データ週数</div>
                </div>
            </div>
            
            {f'''
            <div class="stats-summary" style="margin-top: 20px; background: #fff3cd; border: 1px solid #ffeaa7;">
                <div class="stat-item">
                    <div class="stat-value" style="color: #e74c3c;">{prediction_info.get('predicted_total', 'N/A')}</div>
                    <div class="stat-label">2025年予測最終</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color: #e74c3c;">{prediction_info.get('additional_predicted', 'N/A')}</div>
                    <div class="stat-label">予測追加数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color: #e74c3c;">{prediction_info.get('remaining_games', 'N/A')}</div>
                    <div class="stat-label">残り試合数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" style="color: #e74c3c;">{prediction_info.get('prediction_rate', 'N/A')}</div>
                    <div class="stat-label">週次予測率</div>
                </div>
            </div>
            ''' if prediction_info else ''}
            
            <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #3498db;">
                <h4 style="color: #2c3e50; margin-bottom: 15px; font-size: 18px;">📊 予測について</h4>
                <div style="font-size: 14px; color: #34495e; line-height: 1.6;">
                    <p style="margin-bottom: 12px;"><strong>予測方法：</strong></p>
                    <ul style="margin-left: 20px; margin-bottom: 15px;">
                        <li>2025年の実績データ（70%の重み）と2024年の参考データ（30%の重み）を組み合わせ</li>
                        <li>週あたりのホームラン平均を計算して残り期間を予測</li>
                        <li>現実的な変動を考慮してランダム性を含めた予測値を算出</li>
                    </ul>
                    <p style="margin-bottom: 8px;"><strong>グラフの見方：</strong></p>
                    <ul style="margin-left: 20px; margin-bottom: 10px;">
                        <li><span style="color: #e74c3c; font-weight: bold;">赤い実線</span>：2025年の実際の成績</li>
                        <li><span style="color: #3498db; font-weight: bold;">青い点線</span>：2025年の予測データ</li>
                        <li><span style="color: #95a5a6; font-weight: bold;">灰色の破線</span>：2024年の実績（参考）</li>
                    </ul>
                    <p style="font-size: 12px; color: #7f8c8d; font-style: italic;">
                        ※予測は統計的な計算に基づくものであり、実際の成績と異なる場合があります
                    </p>
                </div>
            </div>
        </div>
        
        <script>
            const chartData = {json.dumps(week_comparison_data)};
            const predictionInfo = {json.dumps(prediction_info)};
            
            // 2025年のデータを実績と予測に分ける
            const currentWeek = predictionInfo.current_week || 23;
            const weeks2025 = chartData.weeks;
            const data2025 = chartData['2025'];
            
            // 実績データ（現在の週まで）
            const actualWeeks = weeks2025.filter(w => w <= currentWeek);
            const actualData = data2025.slice(0, actualWeeks.length);
            
            // 予測データ（現在の週から最後まで）
            const predictionWeeks = weeks2025.filter(w => w >= currentWeek);
            const predictionData = data2025.slice(actualWeeks.length - 1); // 接続のため1つ前から開始
            
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
            
            const trace2025Actual = {{
                x: actualWeeks,
                y: actualData,
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
                name: '2025年（実績）'
            }};
            
            const trace2025Prediction = {{
                x: predictionWeeks,
                y: predictionData,
                type: 'scatter',
                mode: 'lines+markers',
                line: {{
                    color: '#3498db',
                    width: 3,
                    dash: 'dot'
                }},
                marker: {{
                    color: '#3498db',
                    size: 6
                }},
                name: '2025年（予測）'
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
            
            Plotly.newPlot('chart', [trace2024, trace2025Actual, trace2025Prediction], layout, config);
        </script>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    # Heroku用の設定
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)

