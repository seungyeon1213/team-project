# 파일명: real_crowd_safety.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="압사 예방 실전", layout="wide")
st.title("🚨 압사 예방 실전 시뮬레이터")

# ----------------------------
# 1. 사용자 위치 입력 (실전 환경에서는 GPS 자동 연동)
# ----------------------------
st.header("1️⃣ 현재 위치")
user_lat = st.number_input("위도", value=37.5665, format="%.6f")
user_lon = st.number_input("경도", value=126.9780, format="%.6f")
st.write(f"📍 현재 위치: ({user_lat}, {user_lon})")

# ----------------------------
# 2. 주변 군중 밀집도 시뮬레이션 (실전: API 연동)
# ----------------------------
st.header("2️⃣ 주변 군중 밀집도 확인")
zones = [{"name": f"구역{i+1}", 
          "lat": user_lat + random.uniform(-0.002,0.002),
          "lon": user_lon + random.uniform(-0.002,0.002),
          "crowd": random.randint(20,100)} for i in range(5)]

RISK_THRESHOLD = 70  # 위험 임계치

# ----------------------------
# 3. 지도 표시
# ----------------------------
m = folium.Map(location=[user_lat, user_lon], zoom_start=17)
# 사용자 위치 표시
folium.Marker([user_lat, user_lon], popup="내 위치", icon=folium.Icon(color="blue")).add_to(m)
# 구역 표시
for z in zones:
    color = "red" if z["crowd"] >= RISK_THRESHOLD else "green"
    folium.CircleMarker([z["lat"], z["lon"]],
                        radius=15,
                        color=color,
                        fill=True,
                        fill_opacity=0.6,
                        popup=f"{z['name']} - 밀집도: {z['crowd']}").add_to(m)

st_folium(m, width=700, height=500)

# ----------------------------
# 4. 즉시 위험 알림
# ----------------------------
st.header("3️⃣ 위험 알림")
high_risk_zones = [z for z in zones if z["crowd"] >= RISK_THRESHOLD]

if high_risk_zones:
    st.markdown("""
    <script>
    // 소리 재생
    new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg").play();
    // 진동
    if (navigator.vibrate) { navigator.vibrate([500,200,500]); }
    </script>
    """, unsafe_allow_html=True)
    
    st.warning("⚠️ 주변 구역 혼잡! 접근 금지!")
    for z in high_risk_zones:
        st.write(f"- {z['name']} 밀집도: {z['crowd']}")
else:
    st.success("✅ 주변 안전")

# ----------------------------
# 5. 한 번 누르기 신고
# ----------------------------
st.header("4️⃣ 위험 신고")
if st.button("🚨 위험 신고"):
    # 실제 구현 시 서버/DB로 위치+위험 정보 전송 가능
    st.error("신고 완료! 위치와 위험 정보가 전송되었습니다.")
