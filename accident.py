pip install streamlit folium streamlit-folium
# 파일명: crowd_safety_simulator.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="압사 예방 시뮬레이터", layout="wide")

st.title("🚨 압사 예방 최소 기능 시뮬레이터")

# ----------------------------
# 1. 사용자 위치 (테스트용 랜덤 위치 생성)
# ----------------------------
st.header("1️⃣ 현재 위치 확인")
# 실제 구현 시 GPS 연동 필요
user_lat = st.number_input("현재 위도", value=37.5665)
user_lon = st.number_input("현재 경도", value=126.9780)

st.write(f"📍 현재 위치: ({user_lat}, {user_lon})")

# ----------------------------
# 2. 주변 군중 밀집 시뮬레이션
# ----------------------------
st.header("2️⃣ 주변 군중 밀집 경고")

# 주변 도로/구역 예시 생성
# 실제 구현 시 CCTV/센서/인원 데이터 연동 필요
zones = [
    {"name": "도로 A", "lat": user_lat+0.001, "lon": user_lon+0.001},
    {"name": "도로 B", "lat": user_lat+0.002, "lon": user_lon-0.001},
    {"name": "광장", "lat": user_lat-0.001, "lon": user_lon+0.002}
]

# 각 구역 밀집도 0~100 임의 생성 (실제 구현 시 데이터 연동)
for zone in zones:
    zone["crowd"] = random.randint(20, 100)

# 위험 임계치 설정
RISK_THRESHOLD = 70

# 지도 표시
m = folium.Map(location=[user_lat, user_lon], zoom_start=17)

# 사용자 위치 표시
folium.Marker(
    [user_lat, user_lon],
    popup="내 위치",
    icon=folium.Icon(color="blue", icon="user")
).add_to(m)

# 구역 표시
for zone in zones:
    color = "red" if zone["crowd"] >= RISK_THRESHOLD else "green"
    folium.CircleMarker(
        location=[zone["lat"], zone["lon"]],
        radius=15,
        color=color,
        fill=True,
        fill_opacity=0.6,
        popup=f"{zone['name']} - 밀집도: {zone['crowd']}"
    ).add_to(m)

st_folium(m, width=700, height=500)

# ----------------------------
# 3. 즉시 위험 알림
# ----------------------------
st.header("3️⃣ 위험 알림")
high_risk_zones = [z for z in zones if z["crowd"] >= RISK_THRESHOLD]

if high_risk_zones:
    st.warning("⚠️ 주변에 혼잡 구역이 있습니다! 접근하지 마세요!")
    for z in high_risk_zones:
        st.write(f"- {z['name']} 밀집도: {z['crowd']}")
else:
    st.success("✅ 주변 구역 안전")

# ----------------------------
# 4. 한 번 누르기 신고 기능
# ----------------------------
st.header("4️⃣ 신고하기 (한 번 클릭으로 가능)")
if st.button("🚨 위험 신고"):
    st.error("신고 완료! 위치와 위험 정보가 관리자/참여자에게 전송되었습니다.")
    # 실제 구현 시 서버/DB로 위치+위험 전송
