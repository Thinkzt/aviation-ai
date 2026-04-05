"""
AviationAI - 气象数据API封装
统一接口，适配多数据源
"""
import requests
import sqlite3
from datetime import datetime

class WeatherAPI:
    """气象数据统一接口"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or "/tmp/aviation_weather.db"
        self.init_db()
        
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY,
                airport TEXT,
                timestamp TEXT,
                temperature REAL,
                wind_speed REAL,
                wind_dir REAL,
                visibility REAL,
                pressure REAL,
                source TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def fetch_openmeteo(self, lat, lon):
        """Open-Meteo数据源"""
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m,wind_direction_10m,visibility"
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            return {
                "temperature": data["current"]["temperature_2m"],
                "wind_speed": data["current"]["wind_speed_10m"],
                "wind_dir": data["current"]["wind_direction_10m"],
                "visibility": data["current"]["visibility"],
                "source": "open-meteo"
            }
        except Exception as e:
            return None
    
    def save_weather(self, airport, data):
        """保存气象数据"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO weather (airport, timestamp, temperature, wind_speed, wind_dir, visibility, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            airport,
            datetime.now().isoformat(),
            data.get("temperature"),
            data.get("wind_speed"),
            data.get("wind_dir"),
            data.get("visibility"),
            data.get("source", "unknown")
        ))
        conn.commit()
        conn.close()
    
    def get_latest(self, airport=None):
        """获取最新数据"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if airport:
            c.execute("""
                SELECT * FROM weather WHERE airport=? 
                ORDER BY timestamp DESC LIMIT 1
            """, (airport,))
        else:
            c.execute("""
                SELECT airport, MAX(timestamp), temperature, wind_speed, visibility
                FROM weather GROUP BY airport
            """)
        return c.fetchall()
        conn.close()
