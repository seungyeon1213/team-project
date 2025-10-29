import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json

st.set_page_config(page_title="압사 예방 실전", layout="wide")
st.title("🚨 압사 예방 실전 시뮬레이터")

# --- 1. GPS 자동 연동 (JS 브라우저 위치 API)
st.markdown("""
<script>
navigator.geolocation.getCurrentPosition(
    (position) => {
        document.querySelector('#latitude').value = position.coords.latitude;
        document.querySelector('#longitude').value = position.coords.longitude;
    }
);
</script>
""", unsafe_allow_html=True)

user_lat = st.number_input("위도", key="latitude", format="%.6f")
user_lon = st.number_input("경도", key="longitude", format="%.6f")

# --- 2. 주변 밀집도 API 호출 (예: 공공 API)
# 실제 환경에서는 공식 센서/인원 데이터 API 연동
# 예시: /api/crowd_density?lat=...&lon=...
# 아래는 테스트용 랜덤값
import random
zones = [{"name": f"구역{i}", 
          "lat": user_lat+random.uniform(-0.002,0.002),
          "lon": user_lon+random.uniform(-0.002,0.002),
          "crowd": random.randint(20,100)} for i in range(5)]

RISK_THRESHOLD = 70

# --- 3. 지도 시각화
m = folium.Map(location=[user_lat, user_lon], zoom_start=17)
folium.Marker([user_lat, user_lon], popup="내 위치", icon=folium.Icon(color="blue")).add_to(m)
for z in zones:
    color = "red" if z["crowd"]>=RISK_THRESHOLD else "green"
    folium.CircleMarker([z["lat"], z["lon"]], radius=15, color=color,
                        fill=True, fill_opacity=0.6,
                        popup=f"{z['name']} - 밀집도 {z['crowd']}").add_to(m)
st_folium(m, width=700, height=500)

# --- 4. 위험 알림 + 소리/진동
high_risk = [z for z in zones if z["crowd"]>=RISK_THRESHOLD]
if high_risk:
    st.markdown("""
    <script>
    new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg").play();
    window.navigator.vibrate(500);
    </script>
    """, unsafe_allow_html=True)
    st.warning("⚠️ 주변 구역 혼잡! 접근 금지!")
    for z in high_risk:
        st.write(f"- {z['name']} 밀집도: {z['crowd']}")
else:
    st.success("✅ 주변 안전")

# --- 5. 한 번 누르기 신고
if st.button("🚨 위험 신고"):
    # 실제 구현 시 서버에 POST 요청 전송
    # 예: requests.post("https://yourserver.com/report", json={"lat":user_lat,"lon":user_lon,"risk":high_risk})
    st.error("신고 완료! 위치와 위험 정보 전송됨")
