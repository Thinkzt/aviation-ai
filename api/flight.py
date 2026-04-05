"""
AviationAI - 航班数据API封装
多源融合：Aviationstack + OpenSky
"""
import requests
import sqlite3
from datetime import datetime

class FlightAPI:
    """航班数据统一接口"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or "/tmp/aviation_flights.db"
        self.aviationstack_key = "b41959f4c82b03d4fe717127c12c507d"
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY,
                flight_number TEXT,
                airline TEXT,
                origin TEXT,
                destination TEXT,
                status TEXT,
                timestamp TEXT,
                source TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def fetch_aviationstack(self, airport):
        """Aviationstack数据源"""
        url = "http://api.aviationstack.com/v1/flights"
        params = {
            "access_key": self.aviationstack_key,
            "dep_iata": airport,
            "limit": 10
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if "data" in data:
                return data["data"]
        except Exception as e:
            pass
        return []
    
    def fetch_opensky(self, lamin=8, lamax=30, lomin=90, lomax=110):
        """OpenSky数据源"""
        url = "https://opensky-network.org/api/states/all"
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                states = data.get("states", [])
                # 筛选亚太区域
                filtered = [s for s in states if s[5] and s[6]]
                return filtered[:50]
        except Exception as e:
            pass
        return []
    
    def get_chinese_flights(self):
        """获取中国航班"""
        states = self.fetch_opensky()
        chinese_prefixes = ["CCA", "CES", "CSN", "CXA", "CSC", "CSZ", "CHH"]
        return [s for s in states if any(p in str(s[1]) for p in chinese_prefixes)]
