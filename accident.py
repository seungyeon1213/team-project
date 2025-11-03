# 파일명: safetrip_v9_lite.py
import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="SafeTrip v9 Lite", page_icon="✈️", layout="wide")

st.title("✈️ SafeTrip Lite 버전")
st.caption("기존 기능 + 외교부 경보 + 환율 표시 (간결 버전)")

st.markdown("---")

# ✅ 기본 데이터
safety_data = {
    "한국": {
        "도시": ["서울", "부산"],
        "위험 정보": ["대체로 안전"],
        "대처 요령": ["일반 안전 수칙 준수"],
        "현지 연락처": {"긴급 전화": "112"},
    },
    "일본": {
        "도시": ["도쿄", "오사카"],
        "위험 정보": ["지진 발생 가능성"],
        "대처 요령": ["지진 대피 요령 숙지"],
        "현지 연락처": {"긴급 전화": "110"},
    },
    "태국": {
        "도시": ["방콕", "푸켓"],
        "위험 정보": ["소매치기 주의"],
        "대처 요령": ["소지품 주의"],
        "현지 연락처": {"긴급 전화": "191"},
    },
    "프랑스": {
        "도시": ["파리", "니스"],
        "위험 정보": ["시위 및 소매치기 주의"],
        "대처 요령": ["가방은 앞으로 메기"],
        "현지 연락처": {"긴급 전화": "17"},
    },
}

# ✅ 외교부 여행경보 (샘플 데이터)
alert_level = {
    "한국": "1단계 (일반)",
    "일본": "1단계 (일반)",
    "태국": "2단계 (여행 유의)",
    "프랑스": "2단계 (여행 유의)",
}

# ✅ 환율 표시용 함수
currency_codes = {"한국": "KRW", "일본": "JPY", "태국": "THB", "프랑스": "EUR"}

def get_exchange_rate(target_currency):
    try:
        res = requests.get(f"https://api.exchangerate.host/convert?from=KRW&to={target_currency}").json()
        return res.get("result", None)
    except:
        return None

# ✅ 체크리스트 항목
check_list = ["여권/비자 확인", "보험 가입", "비상연락망 저장", "신용카드 분실 신고처 메모"]

# ✅ 세션 상태 초기화
if "travel_history" not in st.session_state:
    st.session_state.travel_history = []
if "checklist" not in st.session_state:
    st.session_state.checklist = {}

# ✅ 국가 / 도시 선택
col1, col2 = st.columns(2)
with col1:
    country = st.selectbox("🌍 국가 선택", list(safety_data.keys()))
with col2:
    city = st.selectbox("🏙️ 도시 선택", safety_data[country]["도시"])

if st.button("🔍 여행 안전 보고서 보기", type="primary"):
    st.session_state.travel_history.append({"국가": country, "도시": city, "날짜": datetime.date.today()})
    if country not in st.session_state.checklist:
        st.session_state.checklist[country] = {c: False for c in check_list}
    st.session_state["selected_country"] = country
    st.session_state["selected_city"] = city
    st.session_state["report_on"] = True
    st.rerun()

# ✅ 보고서 화면
if "report_on" in st.session_state and st.session_state["report_on"]:
    country = st.session_state["selected_country"]
    city = st.session_state["selected_city"]
    info = safety_data[country]

    st.header(f"📋 {country} - {city} 안전 보고서")
    st.info(f"🌐 외교부 여행경보: **{alert_level.get(country, '정보 없음')}**")

    # 환율 표시
    if country in currency_codes and country != "한국":
        rate = get_exchange_rate(currency_codes[country])
        if rate:
            st.metric("💱 환율", f"1,000 KRW ≈ {rate*1000:.2f} {currency_codes[country]}")
        else:
            st.warning("환율 정보를 불러올 수 없습니다.")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚠️ 위험 정보")
        for r in info["위험 정보"]:
            st.warning(r)

    with col2:
        st.subheader("✅ 대처 요령")
        for t in info["대처 요령"]:
            st.success(t)

    st.markdown("---")
    st.subheader("🧳 여행 전 점검")
    checklist = st.session_state.checklist[country]
    for item in check_list:
        checklist[item] = st.checkbox(item, checklist[item], key=f"{country}_{item}")

    done = sum(checklist.values())
    total = len(check_list)
    if done < total:
        st.warning(f"⚠️ {done}/{total} 항목 완료 — 출국 전 점검이 필요합니다.")
    else:
        st.success("🎉 모든 점검 완료!")

    if st.button("⬅️ 처음으로 돌아가기"):
        st.session_state["report_on"] = False
        st.rerun()

st.markdown("---")
st.subheader("📜 나의 여행 기록")
if len(st.session_state.travel_history) > 0:
    st.dataframe(pd.DataFrame(st.session_state.travel_history))
else:
    st.info("아직 여행 기록이 없습니다.")
