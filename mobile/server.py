#!/usr/bin/env python3
"""
AviationAI Mobile Backend Server
云南航务监控移动端后端服务
"""

import asyncio
import json
import re
from datetime import datetime
from aiohttp import web
import aiohttp
import time

# ========== 云南机场配置 ==========
AIRPORTS = {
    'ZPPP': {'name': '昆明长水', 'lat': 25.1, 'lon': 102.9},
    'ZPLJ': {'name': '丽江三义', 'lat': 26.7, 'lon': 100.2},
    'ZPDL': {'name': '大理凤仪', 'lat': 25.6, 'lon': 100.3},
    'ZPJH': {'name': '西双版纳', 'lat': 21.9, 'lon': 100.8},
    'ZPMS': {'name': '德宏芒市', 'lat': 24.4, 'lon': 98.5},
    'ZATC': {'name': '腾冲驼峰', 'lat': 25.0, 'lon': 98.5},
    'ZPSM': {'name': '保山云瑞', 'lat': 25.1, 'lon': 99.2},
    'ZUTC': {'name': '昭通', 'lat': 27.3, 'lon': 103.7},
    'ZPDQ': {'name': '迪庆香格里拉', 'lat': 27.8, 'lon': 99.7},
}

# ========== 气象数据缓存 ==========
weather_cache = {}
cache_timeout = 60  # 秒

# ========== API路由 ==========

async def get_metar(request):
    """获取METAR气象报文"""
    icao = request.match_info.get('icao', 'ZPPP').upper()
    
    # 检查缓存
    now = time.time()
    if icao in weather_cache and now - weather_cache[icao]['time'] < cache_timeout:
        return web.json_response(weather_cache[icao]['data'])
    
    try:
        # 尝试NOAA气象源
        url = f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{icao}.TXT"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    data = parse_metar(text, icao)
                    weather_cache[icao] = {'time': now, 'data': data}
                    return web.json_response(data)
    except Exception as e:
        print(f"METAR error: {e}")
    
    # 返回模拟数据
    return web.json_response(get_mock_weather(icao))

async def get_taf(request):
    """获取TAF预报"""
    icao = request.match_info.get('icao', 'ZPPP').upper()
    return web.json_response({'taf': f'TAF {icao} {get_mock_taf(icao)}'})

async def get_flights(request):
    """获取机场航班"""
    icao = request.match_info.get('icao', 'ZPPP').upper()
    return web.json_response({'flights': get_mock_flights(icao)})

async def get_opensky(request):
    """获取OpenSky全球航班"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://opensky-network.org/api/states/all', timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return web.json_response({'states': data.get('states', [])})
    except Exception as e:
        print(f"OpenSky error: {e}")
    return web.json_response({'states': []})

# ========== 数据解析 ==========

def parse_metar(text, icao):
    """解析METAR报文"""
    try:
        lines = text.strip().split('\n')
        metar = lines[-1] if lines else ''
        
        # 简单解析
        temp_match = re.search(r'(\d{2})/(\d{2})', metar)
        wind_match = re.search(r'(\d{3}|VRB)(\d{2})KT', metar)
        vis_match = re.search(r'(9999|\d{4})', metar)
        cld_match = re.search(r'(FEW|SCT|BKN|OVC)(\d{3})', metar)
        
        temp = f"{temp_match.group(1)}degC" if temp_match else '--degC'
        wind = f"{wind_match.group(2)}m/s" if wind_match else '--m/s'
        vis = f"{vis_match.group(1)}m" if vis_match else '--m'
        cld = f"{cld_match.group(2)}00ft" if cld_match else 'NSC'
        
        return {
            'icao': icao,
            'time': datetime.now().strftime('%H:%M'),
            'temp': temp,
            'wind': wind,
            'vis': vis,
            'cld': cld,
            'raw': metar
        }
    except Exception as e:
        return get_mock_weather(icao)

def get_mock_weather(icao):
    """生成模拟气象数据"""
    base = {
        'ZPPP': {'temp': '18degC', 'wind': '3m/s SE', 'vis': '5000m', 'cld': '3000ft'},
        'ZPLJ': {'temp': '12degC', 'wind': '5m/s NW', 'vis': '8000m', 'cld': '4500ft'},
        'ZPDL': {'temp': '15degC', 'wind': '2m/s', 'vis': '6000m', 'cld': '2500ft'},
        'ZPJH': {'temp': '25degC', 'wind': '2m/s', 'vis': '9999m', 'cld': '无云'},
        'ZPMS': {'temp': '20degC', 'wind': '4m/s', 'vis': '4000m', 'cld': '2000ft'},
        'ZPDQ': {'temp': '8degC', 'wind': '6m/s', 'vis': '7000m', 'cld': '3500ft'},
    }
    return {
        'icao': icao,
        'time': datetime.now().strftime('%H:%M'),
        **(base.get(icao, base['ZPPP']))
    }

def get_mock_taf(icao):
    hour = datetime.now().hour
    return f"{hour:02d}Z 2506G15KT 8000 HZ BECMG {hour+2:02d}00/{hour+4:02d}00 5000 BR NSC="

def get_mock_flights(icao):
    """生成模拟航班数据"""
    flights = {
        'ZPPP': [
            {'callsign': 'MU9645', 'from': 'KMG', 'to': 'VTE', 'altitude': 35000},
            {'callsign': 'MU5686', 'from': 'KMG', 'to': 'TAO', 'altitude': 38000},
            {'callsign': 'KY6617', 'from': 'KMG', 'to': 'SZX', 'altitude': 33000},
        ],
        'ZPLJ': [
            {'callsign': 'QH801', 'from': 'LJG', 'to': 'HAN', 'altitude': 36000},
        ],
    }
    return flights.get(icao, [])

# ========== WebSocket实时推送 ==========

async def websocket_handler(request):
    """WebSocket实时数据推送"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            if data.get('type') == 'subscribe':
                icao = data.get('icao', 'ZPPP')
                # 每5秒推送一次
                while True:
                    await asyncio.sleep(5)
                    weather = get_mock_weather(icao)
                    await ws.send_json(weather)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break
    
    return ws

# ========== 主服务器 ==========

async def index(request):
    """前端页面"""
    with open('dist/index.html', 'r') as f:
        return web.Response(text=f.read(), content_type='text/html')

def create_app():
    app = web.Application()
    
    # API路由
    app.router.add_get('/api/metar/{icao}', get_metar)
    app.router.add_get('/api/taf/{icao}', get_taf)
    app.router.add_get('/api/flights/{icao}', get_flights)
    app.router.add_get('/api/opensky', get_opensky)
    app.router.add_get('/ws', websocket_handler)
    
    # 前端静态文件
    app.router.add_get('/', index)
    app.router.add_static('/assets', 'dist/assets')
    
    return app

if __name__ == '__main__':
    print("✈️ AviationAI Mobile Server")
    print("=" * 40)
    print("本地访问: http://localhost:5174")
    print("云南机场: ZPPP/ZPLJ/ZPDL/ZPJH/ZPMS/ZPDQ")
    print("=" * 40)
    
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=5174)
