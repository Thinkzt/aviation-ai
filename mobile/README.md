# AviationAI Mobile - 航务监控掌中宝

> 云南机场航务监控移动端 | 璇玑史出品

## 功能特性

| 功能 | 说明 |
|------|------|
| 🌤️ 气象实况 | METAR/TAF实时监控 |
| 🛫 航班动态 | OpenSky全球航班追踪 |
| 🚨 告警推送 | 低能见度/大风预警 |
| 📱 移动优先 | 分辨率自适应 |
| 🔄 自动更新 | 后台静默升级 |

## 快速部署

### 方式1: Docker部署 (推荐)
```bash
# 构建镜像
docker build -t aviation-ai-mobile .

# 运行容器
docker run -d -p 5174:5174 --name aviation-ai-mobile aviation-ai-mobile

# 访问
open http://localhost:5174
```

### 方式2: 本地开发
```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 启动后端
python server.py
```

## 云南机场支持

| ICAO | 机场名称 |
|------|---------|
| ZPPP | 昆明长水国际机场 |
| ZPLJ | 丽江三义国际机场 |
| ZPDL | 大理凤仪机场 |
| ZPJH | 西双版纳嘎洒国际机场 |
| ZPMS | 德宏芒市机场 |
| ZPDQ | 迪庆香格里拉机场 |

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Pinia |
| 后端 | Python 3 aiohttp |
| 数据 | NOAA METAR / OpenSky |
| 部署 | Docker |

## 版本计划

| 版本 | 日期 | 内容 |
|------|------|------|
| v0.1.0 | 2026-04-05 | 基础框架搭建 |
| v0.2.0 | 2026-04-19 | 完整UI + API对接 |
| v0.3.0 | 2026-05-03 | APK打包发布 |

## 团队分工

| 角色 | 负责人 | 职责 |
|------|--------|------|
| CEO | 璇玑史 | 决策升级方向 |
| 开发 | 织锦 | 代码重构/GUI开发 |
| 民航专家 | 天枢 | 航务逻辑优化 |
| 数据官 | 磐石 | API封装/数据模型 |
| 进化引擎 | 薪火 | 版本迭代/发布 |

---

**✈️ AviationAI - 让航务监控触手可及**
