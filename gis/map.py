"""
AviationAI - GIS地图模块
基于Leaflet的航班轨迹+气象叠加展示
"""
import json
from datetime import datetime

class GISMap:
    """GIS地图生成器"""
    
    def __init__(self):
        self.center = [25.0, 102.0]  # 云南中心
        self.zoom = 6
        
    def generate_html(self, airports, flights, weather):
        """生成Leaflet地图HTML"""
        return f'''
<!DOCTYPE html>
<html>
<head>
    <title>AviationAI GIS</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #map {{ height: 600px; width: 100%; }}
        .legend {{ background: white; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([{self.center[0]}, {self.center[1]}], {self.zoom});
        
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap'
        }}).addTo(map);
        
        // 机场标记
        var airportIcon = L.divIcon({{className: 'airport-icon', html: '🛫', iconSize: [20,20]}});
        {self._add_airports_js(airports)}
        
        // 航班标记
        {self._add_flights_js(flights)}
        
        // 气象标记
        {self._add_weather_js(weather)}
    </script>
</body>
</html>
        '''
    
    def _add_airports_js(self, airports):
        """生成机场JS代码"""
        lines = []
        for icao, info in airports.items():
            lines.append(f'''
        L.marker([{info['lat']}, {info['lon']}], {{icon: airportIcon}})
            .addTo(map)
            .bindPopup('<b>{info["name"]}</b><br>ICAO: {icao}<br>等级: {info["type"]}');
            ''')
        return ''.join(lines)
    
    def _add_flights_js(self, flights):
        """生成航班JS代码"""
        lines = []
        for i, flight in enumerate(flights[:20]):
            lat, lon = flight.get("lat", 0), flight.get("lon", 0)
            lines.append(f'''
        L.circleMarker([{lat}, {lon}], {{radius: 3, color: 'blue'}})
            .addTo(map)
            .bindPopup('Flight: {flight.get("callsign", "N/A")}');
            ''')
        return ''.join(lines)
    
    def _add_weather_js(self, weather):
        """生成气象JS代码"""
        lines = []
        for w in weather[:10]:
            lat, lon = w.get("lat", 0), w.get("lon", 0)
            color = "green" if w.get("visibility", 10) > 5 else "orange" if w.get("visibility", 10) > 1 else "red"
            lines.append(f'''
        L.circleMarker([{lat}, {lon}], {{radius: 10, color: '{color}', fillOpacity: 0.3}})
            .addTo(map)
            .bindPopup('Wind: {w.get("wind_speed", 0)}m/s');
            ''')
        return ''.join(lines)
    
    def save_html(self, filename, airports, flights, weather):
        """保存地图HTML"""
        html = self.generate_html(airports, flights, weather)
        with open(filename, 'w') as f:
            f.write(html)
        return filename
