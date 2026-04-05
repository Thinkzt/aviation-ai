"""
AviationAI - AI模型模块
风险分析 + 预警决策支持
"""
import random
import hashlib
from datetime import datetime

class RiskAnalyzer:
    """风险分析器"""
    
    # 云南高原阈值
    THRESHOLDS = {
        "wind": 15,      # 大风阈值(m/s)
        "visibility": 1500,  # 低能见度(m)
        "temperature": 0,   # 冰雪温度(°C)
    }
    
    def __init__(self):
        self.alerts = []
        
    def analyze_weather(self, weather_data):
        """分析气象数据，输出风险等级"""
        risks = []
        
        wind = weather_data.get("wind_speed", 0)
        vis = weather_data.get("visibility", 10000)
        temp = weather_data.get("temperature", 20)
        
        # 大风风险
        if wind > self.THRESHOLDS["wind"]:
            risks.append({
                "level": "HIGH",
                "type": "大风",
                "value": f"{wind}m/s",
                "threshold": f">{self.THRESHOLDS['wind']}m/s",
                "suggestion": "跑道入口减速，注意侧风"
            })
        elif wind > self.THRESHOLDS["wind"] * 0.8:
            risks.append({
                "level": "MEDIUM",
                "type": "大风",
                "value": f"{wind}m/s",
                "suggestion": "注意监测"
            })
            
        # 低能见度风险
        if vis < self.THRESHOLDS["visibility"]:
            risks.append({
                "level": "HIGH",
                "type": "低能见度",
                "value": f"{vis}m",
                "threshold": f"<{self.THRESHOLDS['visibility']}m",
                "suggestion": "II类运行准备"
            })
            
        # 冰雪风险
        if temp < self.THRESHOLDS["temperature"]:
            risks.append({
                "level": "HIGH", 
                "type": "冰雪",
                "value": f"{temp}°C",
                "suggestion": "跑道除冰检查"
            })
            
        return risks
    
    def get_risk_level(self, risks):
        """综合风险等级"""
        if any(r["level"] == "HIGH" for r in risks):
            return "🔴 高风险"
        elif any(r["level"] == "MEDIUM" for r in risks):
            return "🟡 中风险"
        return "🟢 正常"
    
    def generate_report(self, airport, weather, risks):
        """生成风险报告"""
        return {
            "airport": airport,
            "timestamp": datetime.now().isoformat(),
            "risk_level": self.get_risk_level(risks),
            "risks": risks,
            "weather": weather,
            "recommendations": [r["suggestion"] for r in risks]
        }
