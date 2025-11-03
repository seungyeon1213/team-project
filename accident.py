# 파일명: safetrip_app_v9_pro.py
import streamlit as st
import pandas as pd
import random
import datetime
import requests
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="SafeTrip Pro (V9)",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ SafeTrip Pro: 여행 안전 보고서 (v9 확장판)")
st.caption("🌐 외교부 여행경보 + 환율 + 안전지수 + 여행이력 기능 통합")

st.markdown("---")

# --- 1. 기본 데이터 (기존 유지) ---
safety_data = {
    "한국": {"도시": ["서울", "부산"], "위험 정보": ["대체로 안전"], "대처 요령": ["일반 안전 수칙 준수"], "현지 연락처": {"긴급 전화": "112"}, "추천": {"명소": ["경복궁"], "맛집": ["명동교자"], "핫플": ["홍대"]}},
    "일본": {"도시": ["도쿄", "오사카"], "위험 정보": ["지진 가능성"], "대처 요령": ["지진 시 대피 요령 숙지"], "현지 연락처": {"긴급 전화": "110"}, "추천": {"명소": ["후지산"], "맛집": ["라멘"], "핫플": ["시부야"]}},
    "태국": {"도시": ["방콕", "푸켓"], "위험 정보": ["소매치기 주의"], "대처 요령": ["대중교통 이용"], "현지 연락처": {"긴급 전화": "191"}, "추천": {"명소": ["왕궁"], "맛집": ["팟타이"], "핫플": ["카오산로드"]}},
    "프랑스": {"도시": ["파리", "니스"], "위험 정보": ["시위 및 소매치기 주의"], "대처 요령": ["가방은 앞으로 메기"], "현지 연락처": {"긴급 전화": "17"}, "추천": {"명소": ["에펠탑"], "맛집": ["크루아상"], "핫플": ["마레 지구"]}},
}

check_list = [
    "여권/비자 확인", "여행자 보험 가입", "긴급 연락처 저장",
    "신용카드 분실 신고처 메모", "날씨 및 복장 확인", "상비약 준비"
]

# --- 2. 세션 상태 관리 ---
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "한국"
if "selected_city" not in st.session_state:
    st.session_state.selected_city = "서울"
if "checklist_status" not in st.session_state:
    st.session_state.checklist_status = {}
if "travel_history" not in st.session_state:
    st.session_state.travel_history = []
if "report_searched" not in st.session_state:
    st.session_state.report_searched = False

# --- 3. 외교부 여행경보 단계 (샘플 데이터) ---
alert_level = {
    "한국": "1단계 (일반)",
    "일본": "1단계 (일반)",
    "태국": "2단계 (여행 유의)",
    "프랑스": "2단계 (여행 유의)"
}

# --- 4. 국가별 환율 정보 (무료 API 샘플 - exchangerate.host 사용) ---
def get_exchange_rate(target_currency):
    try:
        url = f"https://api.exchangerate.host/convert?from=KRW&to={target_currency}"
        res = requests.get(url).json()
        return res.get("result", None)
    except:
        return None

currency_codes = {"한국": "KRW", "일본": "JPY", "태국": "THB", "프랑스": "EUR"}

# --- 5. 안전지수 (가상 수치 예시) ---
safety_index = {
    "한국": 95,
    "일본": 92,
    "태국": 78,
    "프랑스": 81
}

# --- 6. 국가/도시 선택 ---
col1, col2 = st.columns(2)
with col1:
    selected_country = st.selectbox("🌍 국가 선택", list(safety_data.keys()))
with col2:
    selected_city = st.selectbox("🏙️ 도시 선택", safety_data[selected_country]["도시"])

if st.button("🔍 안전 보고서 보기", type="primary"):
    st.session_state.selected_country = selected_country
    st.session_state.selected_city = selected_city
    st.session_state.report_searched = True
    # 여행 이력에 추가
    record = {"국가": selected_country, "도시": selected_city, "날짜": datetime.date.today()}
    st.session_state.travel_history.append(record)
    # 체크리스트 초기화
    if selected_country not in st.session_state.checklist_status:
        st.session_state.checklist_status[selected_country] = {item: False for item in check_list}
    st.rerun()

# --- 7. 안전 보고서 표시 ---
if st.session_state.report_searched:
    country = st.session_state.selected_country
    city = st.session_state.selected_city
    info = safety_data[country]
    
    st.header(f"📋 {city}, {country} 안전 보고서")
    st.info(f"🌐 외교부 여행경보: **{alert_level.get(country, '정보 없음')}**")

    # 환율 표시
    if country in currency_codes and country != "한국":
        rate = get_exchange_rate(currency_codes[country])
        if rate:
            st.metric(f"💱 1,000 KRW = {rate*1000:.2f} {currency_codes[country]}")
        else:
            st.warning("환율 정보를 불러올 수 없습니다.")
    
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["⚠️ 위험 정보", "✅ 대처 요령", "📝 점검 리스트", "📊 국가별 안전지수"])

    with tab1:
        st.subheader("⚠️ 위험 정보")
        for r in info["위험 정보"]:
            st.warning(r)

    with tab2:
        st.subheader("✅ 대처 요령")
        for t in info["대처 요령"]:
            st.success(t)

    with tab3:
        st.subheader("📝 여행 전 점검")
        checklist = st.session_state.checklist_status[country]
        for item in check_list:
            checklist[item] = st.checkbox(item, checklist[item], key=f"{country}_{item}")
        st.session_state.checklist_status[country] = checklist

        completed = sum(checklist.values())
        total = len(check_list)
        if completed < total:
            st.warning(f"⚠️ {completed}/{total} 항목 완료 — 출국 전 점검이 필요합니다!")
        else:
            st.success("🎉 모든 점검 완료! 안전한 여행 되세요!")

    with tab4:
        st.subheader("📊 국가별 안전지수 비교")
        df = pd.DataFrame(list(safety_index.items()), columns=["국가", "안전지수"])
        st.bar_chart(df.set_index("국가"))

    # 다시 검색 버튼
    if st.button("⬅️ 처음으로 돌아가기"):
        st.session_state.report_searched = False
        st.rerun()

# --- 8. 여행 이력 표시 ---
st.markdown("---")
st.subheader("🧳 나의 여행 기록")
if len(st.session_state.travel_history) > 0:
    df = pd.DataFrame(st.session_state.travel_history)
    st.dataframe(df)
else:
    st.info("아직 여행 기록이 없습니다.")
