<template>
  <div class="app-container">
    <!-- 顶部状态栏 -->
    <header class="header">
      <div class="header-left">
        <span class="logo">✈️</span>
        <span class="title">AviationAI</span>
      </div>
      <div class="header-right">
        <span class="status-dot" :class="apiStatus"></span>
        <span class="time">{{ currentTime }}</span>
      </div>
    </header>

    <!-- 主监控卡片 -->
    <main class="main-content">
      <!-- 机场选择器 -->
      <div class="airport-selector">
        <select v-model="selectedAirport" @change="fetchData">
          <option value="ZPPP">昆明长水</option>
          <option value="ZPLJ">丽江三义</option>
          <option value="ZPDL">大理凤仪</option>
          <option value="ZPJH">西双版纳</option>
          <option value="ZPMS">德宏芒市</option>
          <option value="ZPDQ">迪庆香格里拉</option>
        </select>
      </div>

      <!-- 气象实况卡片 -->
      <div class="card weather-card">
        <div class="card-header">
          <span class="card-title">🌤️ 气象实况</span>
          <span class="update-time">{{ weatherData.time }}</span>
        </div>
        <div class="weather-grid">
          <div class="weather-item">
            <span class="weather-icon">🌡️</span>
            <span class="weather-value">{{ weatherData.temp }}</span>
            <span class="weather-label">温度</span>
          </div>
          <div class="weather-item">
            <span class="weather-icon">💨</span>
            <span class="weather-value">{{ weatherData.wind }}</span>
            <span class="weather-label">风速</span>
          </div>
          <div class="weather-item">
            <span class="weather-icon">👁️</span>
            <span class="weather-value">{{ weatherData.vis }}</span>
            <span class="weather-label">能见度</span>
          </div>
          <div class="weather-item">
            <span class="weather-icon">☁️</span>
            <span class="weather-value">{{ weatherData.cld }}</span>
            <span class="weather-label">云高</span>
          </div>
        </div>
      </div>

      <!-- 告警卡片 -->
      <div class="card alert-card" :class="{ 'has-alert': alerts.length > 0 }">
        <div class="card-header">
          <span class="card-title">🚨 运行提示</span>
          <span class="alert-count" v-if="alerts.length">{{ alerts.length }}</span>
        </div>
        <div class="alert-list">
          <div v-for="(alert, i) in alerts" :key="i" class="alert-item">
            {{ alert }}
          </div>
          <div v-if="!alerts.length" class="no-alert">
            ✅ 运行正常
          </div>
        </div>
      </div>

      <!-- 航班动态卡片 -->
      <div class="card flight-card">
        <div class="card-header">
          <span class="card-title">🛫 航班动态</span>
          <span class="flight-count">{{ flights.length }}架</span>
        </div>
        <div class="flight-list">
          <div v-for="flight in flights.slice(0, 5)" :key="flight.callsign" class="flight-item">
            <div class="flight-info">
              <span class="flight-call">{{ flight.callsign }}</span>
              <span class="flight-route">{{ flight.from }} → {{ flight.to }}</span>
            </div>
            <div class="flight-status">
              <span class="flight-alt">{{ flight.altitude }}ft</span>
            </div>
          </div>
          <div v-if="!flights.length" class="no-flight">
            暂无航班数据
          </div>
        </div>
      </div>

      <!-- TAF预报卡片 -->
      <div class="card taf-card">
        <div class="card-header">
          <span class="card-title">📋 TAF预报</span>
        </div>
        <div class="taf-content">
          {{ tafData }}
        </div>
      </div>
    </main>

    <!-- 底部导航 -->
    <nav class="bottom-nav">
      <div class="nav-item active">
        <span class="nav-icon">🏠</span>
        <span class="nav-label">监控</span>
      </div>
      <div class="nav-item">
        <span class="nav-icon">📊</span>
        <span class="nav-label">数据</span>
      </div>
      <div class="nav-item">
        <span class="nav-icon">⚙️</span>
        <span class="nav-label">设置</span>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const selectedAirport = ref('ZPPP')
const currentTime = ref('')
const apiStatus = ref('offline')

const weatherData = ref({
  time: '--:--',
  temp: '--°C',
  wind: '--m/s',
  vis: '--m',
  cld: '--ft'
})

const alerts = ref([])
const flights = ref([])
const tafData = ref('TAF ZPPP --2406Z --=\n获取中...')

let timeInterval = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const fetchWeather = async () => {
  try {
    // 尝试从本地API获取气象数据
    const res = await axios.get(`/api/weather/${selectedAirport.value}`, { timeout: 5000 }).catch(() => null)
    if (res?.data) {
      weatherData.value = res.data
      apiStatus.value = 'online'
    } else {
      // 使用模拟数据演示
      weatherData.value = {
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
        temp: '18°C',
        wind: '3m/s',
        vis: '5000m',
        cld: '3000ft'
      }
      apiStatus.value = 'demo'
    }
  } catch (e) {
    apiStatus.value = 'error'
  }
}

const fetchFlights = async () => {
  try {
    const res = await axios.get(`/api/flights/${selectedAirport.value}`, { timeout: 5000 }).catch(() => null)
    if (res?.data) {
      flights.value = res.data
    }
  } catch (e) {
    // 演示数据
    flights.value = []
  }
}

const checkAlerts = () => {
  alerts.value = []
  if (weatherData.value.vis === '--m') return
  const vis = parseInt(weatherData.value.vis)
  if (vis < 1500) alerts.value.push('⚠️ 低能见度运行')
  if (weatherData.value.wind.includes('12')) alerts.value.push('⚠️ 大风监控')
}

const fetchData = async () => {
  await Promise.all([fetchWeather(), fetchFlights()])
  checkAlerts()
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  fetchData()
  setInterval(fetchData, 300000) // 5分钟刷新
})

onUnmounted(() => {
  if (timeInterval) clearInterval(timeInterval)
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #1a1a2e;
  padding-bottom: 70px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #16213e;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo { font-size: 24px; }
.title { font-size: 18px; font-weight: 600; }

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #666;
}
.status-dot.online { background: #4ade80; }
.status-dot.demo { background: #facc15; }
.status-dot.error { background: #f87171; }

.time { font-size: 14px; color: #94a3b8; }

.main-content { padding: 12px; }

.airport-selector {
  margin-bottom: 12px;
}

.airport-selector select {
  width: 100%;
  padding: 12px;
  background: #16213e;
  border: 1px solid #334155;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
}

.card {
  background: #16213e;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card-title { font-size: 16px; font-weight: 600; }
.update-time { font-size: 12px; color: #94a3b8; }

.weather-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.weather-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  background: #1e293b;
  border-radius: 8px;
}

.weather-icon { font-size: 24px; margin-bottom: 4px; }
.weather-value { font-size: 18px; font-weight: 600; }
.weather-label { font-size: 12px; color: #94a3b8; }

.alert-card.has-alert { border-left: 3px solid #facc15; }

.alert-count {
  background: #facc15;
  color: #000;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}

.alert-list { display: flex; flex-direction: column; gap: 8px; }
.alert-item { padding: 8px; background: #1e293b; border-radius: 6px; font-size: 14px; }
.no-alert { color: #4ade80; text-align: center; padding: 12px; }

.flight-count {
  background: #3b82f6;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.flight-list { display: flex; flex-direction: column; gap: 8px; }
.flight-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #1e293b;
  border-radius: 6px;
}

.flight-call { font-weight: 600; font-size: 14px; }
.flight-route { font-size: 12px; color: #94a3b8; margin-top: 2px; }
.flight-alt { font-size: 12px; color: #60a5fa; }
.no-flight { text-align: center; color: #94a3b8; padding: 12px; }

.taf-content {
  background: #1e293b;
  padding: 12px;
  border-radius: 6px;
  font-family: monospace;
  font-size: 13px;
  white-space: pre-wrap;
  color: #94a3b8;
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background: #16213e;
  padding: 8px 0;
  border-top: 1px solid #334155;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  color: #64748b;
}

.nav-item.active { color: #3b82f6; }
.nav-icon { font-size: 20px; }
.nav-label { font-size: 11px; }
</style>
