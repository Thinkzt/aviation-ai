# 🛫 民航航务大模型 - AviationAI

> 基于AI的民航航务智能监控系统，支持全国机场部署

[![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](https://github.com/Thinkzt/aviation-ai)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 核心功能

- 📡 **实时气象监控** - 15个云南机场 + 全国机场扩展
- ✈️ **航班追踪** - 多源数据融合
- 🗺️ **GIS地图展示** - 航班轨迹+气象叠加
- 🤖 **AI智能分析** - 风险预警+决策支持
- 🔄 **快速部署** - OpenClaw一键部署

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    AviationAI 民航航务大模型                │
├─────────────────────────────────────────────────────────────┤
│  GUI层: Web控制台 + GIS地图 + 数据可视化                   │
├─────────────────────────────────────────────────────────────┤
│  AI层: 风险分析 + 预警推送 + 决策支持                      │
├─────────────────────────────────────────────────────────────┤
│  数据层: 气象 + 航班 + NOTAM + ADS-B                      │
├─────────────────────────────────────────────────────────────┤
│  接入层: Open-Meteo + NOAA + Aviationstack + OpenSky       │
└─────────────────────────────────────────────────────────────┘
```

## 📊 支持机场

### 云南15机场
昆明长水|丽江三义|大理凤仪|版纳嘎洒|德宏芒市|腾冲驼峰|保山云瑞|昭通|临沧博尚|普洱思茅|澜沧景迈|迪庆香格里拉|文山砚山|红河蒙自|怒江六库

### 数据源
| 类型 | 来源 | 状态 |
|------|------|------|
| 气象 | Open-Meteo | ✅ |
| 气象报文 | NOAA | ✅ |
| 航班 | Aviationstack | ✅ |
| 航班追踪 | OpenSky | ✅ |

## 🚀 快速部署

```bash
# 克隆项目
git clone https://github.com/Thinkzt/aviation-ai.git
cd aviation-ai

# 运行GUI
python3 gui/dashboard.py

# 访问 http://localhost:5000
```

## ⚡ OpenClaw部署

```bash
# 在OpenClaw中直接使用
openclaw skill install aviation-ai
```

## 📄 许可证

MIT License

## 👨‍💻 团队

- **主导**: 璇玑史CEO
- **协作**: 元宝COO
- **开发**: 七星战队
