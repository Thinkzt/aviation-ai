#!/usr/bin/env python3
"""
AviationAI - Web控制台 + GIS地图
民航航务大模型 - GUI核心
"""
import sqlite3
import json
from datetime import datetime
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# 机场数据
AIRPORTS = {
    "ZPPP": {"name": "昆明长水", "lat": 25.10, "lon": 102.93, "type": "4F"},
    "ZPLJ": {"name": "丽江三义", "lat": 26.68, "lon": 100.24, "type": "4D"},
    "ZPDL": {"name": "大理凤仪", "lat": 25.65, "lon": 100.19, "type": "4C"},
    "ZPJH": {"name": "版纳嘎洒", "lat": 21.97, "lon": 100.77, "type": "4D"},
    "ZPMS": {"name": "德宏芒市", "lat": 24.40, "lon": 98.48, "type": "4C"},
}

def get_weather_data(icao=None):
    """获取气象数据"""
    conn = sqlite3.connect('/root/.openclaw/workspace/data/yn_airport_weather.db')
    c = conn.cursor()
    
    if icao:
        c.execute("""
            SELECT * FROM weather 
            WHERE airport=? 
            ORDER BY timestamp DESC LIMIT 1
        """, (icao,))
    else:
        c.execute("""
            SELECT airport, MAX(timestamp), temperature, wind_speed, visibility
            FROM weather 
            GROUP BY airport
        """)
    
    results = c.fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/weather')
def api_weather():
    """气象API"""
    data = get_weather_data()
    return jsonify({
        "status": "success",
        "data": data,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/airports')
def api_airports():
    """机场API"""
    return jsonify({
        "status": "success", 
        "airports": AIRPORTS
    })

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AviationAI - 民航航务大模型</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #fff; }
        .header { background: #16213e; padding: 20px; text-align: center; }
        .header h1 { color: #00d4ff; }
        .container { display: flex; height: calc(100vh - 80px); }
        .map { flex: 2; background: #0f3460; position: relative; }
        .sidebar { flex: 1; background: #16213e; padding: 20px; overflow-y: auto; }
        .card { background: #1a1a2e; padding: 15px; margin-bottom: 10px; border-radius: 8px; }
        .card h3 { color: #00d4ff; margin-bottom: 10px; }
        .status { display: inline-block; padding: 2px 8px; border-radius: 4px; }
        .status.ok { background: #00c853; }
        .status.warn { background: #ffc107; }
        .status.error { background: #f44336; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛫 AviationAI - 民航航务大模型</h1>
        <p>全国机场监控 | 实时气象 | 航班追踪 | AI预警</p>
    </div>
    <div class="container">
        <div class="map">
            <div style="padding:20px; text-align:center;">
                <h2>🗺️ GIS地图区域</h2>
                <p>（集成Leaflet地图）</p>
                <div id="map" style="height:400px; background:#0f3460; margin:20px; border-radius:8px;"></div>
            </div>
        </div>
        <div class="sidebar">
            <div class="card">
                <h3>📡 机场状态</h3>
                <div id="airport-list">
                    {% for icao, info in airports.items() %}
                    <div style="margin:5px 0;">
                        <span class="status ok"></span>
                        {{ info.name }} ({{ icao }})
                    </div>
                    {% endfor %}
                </div>
            </div>
            <div class="card">
                <h3>⚠️ 告警信息</h3>
                <div id="alerts">暂无告警</div>
            </div>
            <div class="card">
                <h3>📊 数据统计</h3>
                <p>机场: 5个</p>
                <p>气象: 正常</p>
                <p>航班: 监控中</p>
            </div>
        </div>
    </div>
    <script>
        // 更新机场列表
        fetch('/api/weather')
            .then(r => r.json())
            .then(d => console.log('Data:', d));
    </script>
</body>
</html>
'''

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║  🛫 AviationAI - 民航航务大模型 Web控制台              ║
╠═══════════════════════════════════════════════════════════╣
║  启动服务: http://localhost:5000                         ║
║  按Ctrl+C停止                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
