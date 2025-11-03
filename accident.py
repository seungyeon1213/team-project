# 파일명: safetrip_v9_lite_fixed.py
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="SafeTrip v9 Lite", page_icon="✈️", layout="wide")

st.title("✈️ SafeTrip Lite 버전 (고정 환율 + 확장 국가)")
st.caption("실시간 API 없이 빠르게 동작하는 안전한 여행 도우미")

st.markdown("---")

# ✅ 기본 데이터 (국가 확장 + 캄보디아 추가)
safety_data = {
    "한국": {
        "도시": ["서울", "부산", "제주"],
        "위험 정보": ["대체로 안전", "교통 혼잡 시간 주의"],
        "대처 요령": ["대중교통 이용 권장"],
        "현지 연락처": {"긴급 전화": "112 / 119"},
    },
    "일본": {
        "도시": ["도쿄", "오사카", "후쿠오카", "삿포로"],
        "위험 정보": ["지진 발생 가능성", "유흥가 호객행위 주의"],
        "대처 요령": ["지진 발생 시 DROP, COVER, HOLD ON"],
        "현지 연락처": {"긴급 전화": "110 / 119"},
    },
    "태국": {
        "도시": ["방콕", "푸켓", "치앙마이"],
        "위험 정보": ["관광지 소매치기 주의", "교통 혼잡"],
        "대처 요령": ["공인된 택시 앱 사용"],
        "현지 연락처": {"긴급 전화": "191 / 1669"},
    },
    "베트남": {
        "도시": ["하노이", "호찌민", "다낭"],
        "위험 정보": ["오토바이 교통 혼잡", "소매치기 주의"],
        "대처 요령": ["도로 횡단 시 주의", "현금 대신 카드 사용 권장"],
        "현지 연락처": {"긴급 전화": "113 / 115"},
    },
    "캄보디아": {
        "도시": ["프놈펜", "시엠립"],
        "위험 정보": ["절도, 뎅기열 모기 주의"],
        "대처 요령": ["야간 이동 시 택시 이용"],
        "현지 연락처": {"긴급 전화": "117 / 119"},
    },
    "필리핀": {
        "도시": ["마닐라", "세부", "보라카이"],
        "위험 정보": ["치안 불안 지역 존재", "태풍 주의"],
        "대처 요령": ["여행 전 외교부 경보 확인"],
        "현지 연락처": {"긴급 전화": "911"},
    },
    "인도네시아": {
        "도시": ["발리", "자카르타", "롬복"],
        "위험 정보": ["화산 활동 주의", "교통 혼잡"],
        "대처 요령": ["검증된 교통수단 이용"],
        "현지 연락처": {"긴급 전화": "110 / 118"},
    },
    "호주": {
        "도시": ["시드니", "멜버른", "브리즈번"],
        "위험 정보": ["산불 및 폭우 주의", "독성 생물 주의"],
        "대처 요령": ["야생동물과 거리두기"],
        "현지 연락처": {"긴급 전화": "000"},
    },
    "미국": {
        "도시": ["뉴욕", "LA", "샌프란시스코", "하와이"],
        "위험 정보": ["총기 사건 주의", "야간 치안 불안 지역 존재"],
        "대처 요령": ["인적 드문 지역 피하기"],
        "현지 연락처": {"긴급 전화": "911"},
    },
    "프랑스": {
        "도시": ["파리", "니스", "리옹"],
        "위험 정보": ["소매치기 성행", "시위 발생 가능"],
        "대처 요령": ["가방은 앞으로 메기"],
        "현지 연락처": {"긴급 전화": "17 / 15"},
    },
    "이탈리아": {
        "도시": ["로마", "밀라노", "피렌체"],
        "위험 정보": ["관광지 사기꾼 주의", "소매치기 주의"],
        "대처 요령": ["귀중품 분산 보관"],
        "현지 연락처": {"긴급 전화": "112"},
    },
    "스페인": {
        "도시": ["바르셀로나", "마드리드"],
        "위험 정보": ["소매치기 다발", "시위 및 교통 통제 가능성"],
        "대처 요령": ["지정된 경로 이용"],
        "현지 연락처": {"긴급 전화": "112"},
    },
}

# ✅ 고정 환율 데이터 (2025년 11월 기준, KRW 기준)
exchange_rates = {
    "한국": ("KRW", 1),
    "일본": ("JPY", 0.093),       # 1 JPY = 10.8 KRW → 역변환
    "태국": ("THB", 0.037),       # 1 THB = 27 KRW
    "베트남": ("VND", 0.000053),  # 1 VND = 0.053 KRW
    "캄보디아": ("KHR", 0.00033), # 1 KHR = 3 KRW
    "필리핀": ("PHP", 24.0),      # 1 PHP = 24 KRW
    "인도네시아": ("IDR", 0.000088), # 1 IDR = 0.088 KRW
    "호주": ("AUD", 890.0),       # 1 AUD = 890 KRW
    "미국": ("USD", 1380.0),      # 1 USD = 1380 KRW
    "프랑스": ("EUR", 1470.0),    # 1 EUR = 1470 KRW
    "이탈리아": ("EUR", 1470.0),
    "스페인": ("EUR", 1470.0),
}

# ✅ 여행 전 점검 항목
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
    st.session_state.travel_history.append({
        "국가": country,
        "도시": city,
        "날짜": datetime.date.today()
    })
    if country not in st.session_state.checklist:
        st.session_state.checklist[country] = {c: False for c in check_list}
    st.session_state["selected_country"] = country
    st.session_state["selected_city"] = city
    st.session_state["report_on"] = True
    st.rerun()

# ✅ 보고서 화면
if st.session_state.get("report_on", False):
    country = st.session_state["selected_country"]
    city = st.session_state["selected_city"]
    info = safety_data[country]

    st.header(f"📋 {country} - {city} 안전 보고서")

    # 환율 표시
    code, rate = exchange_rates[country]
    if country == "한국":
        st.metric("💱 환율", "1 KRW = 1 KRW (기준 통화)")
    else:
        st.metric("💱 환율", f"1 {code} ≈ {rate:.3f} KRW")

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
        st.warning(f"⚠️ {done}/{total} 항목 완료 — 출국 전 점검 필요")
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
