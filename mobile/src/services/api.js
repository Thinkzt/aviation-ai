// AviationAI Mobile API Service
// 云南机场航务数据接口

const API_BASE = 'http://localhost:5174/api'

// 云南机场METAR获取
export async function fetchMETAR(icao) {
  try {
    const response = await fetch(`${API_BASE}/metar/${icao}`)
    return await response.json()
  } catch (e) {
    // 离线返回模拟数据
    return getMockWeather(icao)
  }
}

// 云南机场TAF获取
export async function fetchTAF(icao) {
  try {
    const response = await fetch(`${API_BASE}/taf/${icao}`)
    return await response.json()
  } catch (e) {
    return getMockTAF(icao)
  }
}

// 航班追踪
export async function fetchFlights(icao) {
  try {
    const response = await fetch(`${API_BASE}/flights/${icao}`)
    return await response.json()
  } catch (e) {
    return []
  }
}

// OpenSky实时航班
export async function fetchOpenSkyFlights() {
  try {
    const response = await fetch('https://opensky-network.org/api/states/all')
    const data = await response.json()
    return data.states || []
  } catch (e) {
    return []
  }
}

// 模拟气象数据
function getMockWeather(icao) {
  const bases = {
    'ZPPP': { temp: 18, wind: '3m/s SE', vis: '5000m', cld: '3000ft' },
    'ZPLJ': { temp: 12, wind: '5m/s NW', vis: '8000m', cld: '4500ft' },
    'ZPDL': { temp: 15, wind: '2m/s', vis: '6000m', cld: '2500ft' },
    'ZPJH': { temp: 25, wind: '2m/s', vis: '9999m', cld: '无云' },
    'ZPMS': { temp: 20, wind: '4m/s', vis: '4000m', cld: '2000ft' },
    'ZPDQ': { temp: 8, wind: '6m/s', vis: '7000m', cld: '3500ft' },
  }
  return {
    icao,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    ...(bases[icao] || bases['ZPPP'])
  }
}

function getMockTAF(icao) {
  return `TAF ${icao} ${new Date().toISOString().slice(0,10).replace(/-/g,'')}Z 2506G15KT 8000 HZ
       BECMG ${new Date().getHours()+2}00/${new Date().getHours()+4}00 5000 BR NSC=`
}
