# 파일명: safetrip_v10_full.py
import streamlit as st
import pandas as pd
import datetime
import pydeck as pdk

st.set_page_config(page_title="SafeTrip v10 Full", page_icon="✈️", layout="wide")

st.title("✈️ SafeTrip Full 버전 (v10)")
st.caption("여행 일정표 · 지도 · 최신 이슈 · 긴급전화 링크 · 확대 국가/도시 정보 포함")

st.markdown("---")

# --- 기본 데이터 확장 (국가 + 도시 + 위험정보 포함) ---
safety_data = {
    "한국": {
        "도시": ["서울", "부산", "제주", "인천", "대구", "광주", "울산"],
        "위험 정보": ["대체로 안전", "교통 혼잡 시간 주의"],
        "대처 요령": ["대중교통 이용 권장"],
        "현지 연락처": {"긴급 전화": "112 / 119"},
        "추가 이슈": ["최근 소매치기 증가 보고됨"]
    },
    "일본": {
        "도시": ["도쿄", "오사카", "후쿠오카", "삿포로", "교토", "요코하마", "나고야"],
        "위험 정보": ["지진 가능성", "유흥가 호객행위 주의"],
        "대처 요령": ["지진 발생 시 DROP, COVER, HOLD ON"],
        "현지 연락처": {"긴급 전화": "110 / 119"},
        "추가 이슈": ["외국인 대상 유흥가 사기 사례 증가"]
    },
    "태국": {
        "도시": ["방콕", "푸켓", "치앙마이", "파타야", "끄라비", "코사무이"],
        "위험 정보": ["관광지 소매치기 주의", "툭툭 이용 시 가격 흥정 필수"],
        "대처 요령": ["공인된 택시 앱 사용"],
        "현지 연락처": {"긴급 전화": "191 / 1669"},
        "추가 이슈": ["밤늦은 루프탑 바에서 음료 음용 주의"]
    },
    "캄보디아": {
        "도시": ["프놈펜", "시엠립", "시아누크빌", "앙코르", "바탐방"],
        "위험 정보": ["절도 발생 증가", "모기 매개 질병(뎅기열) 주의", "외국인 납치·사기 사례 보고됨"],
        "대처 요령": ["야간 외출 시 택시 이용 권장", "현금 보관 주의"],
        "현지 연락처": {"긴급 전화": "117 / 119"},
        "추가 이슈": ["한국인 대상 유사 납치·사기 경고"]
    },
    "미국": {
        "도시": ["뉴욕", "LA", "샌프란시스코", "하와이", "시카고"],
        "위험 정보": ["도심 일부 지역 범죄율 높음", "법규: 총기 사고 주의"],
        "대처 요령": ["야간에는 인적이 드문 곳 피하기"],
        "현지 연락처": {"긴급 전화": "911"},
        "추가 이슈": ["특정 도시 관광객 대상 범죄 증가 보고됨"]
    },
    "영국": {
        "도시": ["런던", "맨체스터", "에든버러", "리버풀"],
        "위험 정보": ["기차·지하철 지연 가능성", "도심 소매치기 주의"],
        "대처 요령": ["혼잡 시간대 대비", "귀중품 주의"],
        "현지 연락처": {"긴급 전화": "999"},
        "추가 이슈": ["런던 중심가에서 관광객 대상 사기 사례 증가"]
    },
    "호주": {
        "도시": ["시드니", "멜버른", "브리즈번", "퍼스"],
        "위험 정보": ["산불 및 폭우 주의", "환경: 독성 생물 주의"],
        "대처 요령": ["야생동물과의 접촉 자제"],
        "현지 연락처": {"긴급 전화": "000"},
        "추가 이슈": ["해변 이용 시 파도·조류 주의 경고"]
    },
    "베트남": {
        "도시": ["하노이", "호찌민", "다낭", "나트랑"],
        "위험 정보": ["오토바이 교통량 매우 많음", "핸드폰 날치기 주의"],
        "대처 요령": ["길거리 걸을 때 소지품 보호 철저"],
        "현지 연락처": {"긴급 전화": "113 / 115"},
        "추가 이슈": ["관광지 밤거리 안전 주의"]
    },
    "인도네시아": {
        "도시": ["발리", "자카르타", "롬복", "욕야카르타"],
        "위험 정보": ["자연재해: 화산 활동 및 쓰나미 가능성", "교통: 무면허 운전 위험"],
        "대처 요령": ["현지 택시 대신 검증된 교통수단 이용"],
        "현지 연락처": {"긴급 전화": "110 / 118"},
        "추가 이슈": ["외국인 대상 교통사고 증가 보고됨"]
    },
}

# --- 고정 환율 데이터 (원화 기준 환산 예시) ---
# 참고: 실제 환율은 변동하므로 여행시 최신 환율 확인하세요
exchange_rates = {
    "한국": ("KRW", 1, "1원 = 1원"),
    "일본": ("JPY", 0.106, "1원 ≈ 0.106엔"),
    "태국": ("THB", 0.0228, "1원 ≈ 0.0228바트"),
    "캄보디아": ("KHR", 2.83, "1원 ≈ 2.83리엘"),
    "미국": ("USD", 1/1420, "1원 ≈ 0.00070달러"),    # 1 USD ≈ 1,420원 → 1원 ≈ 약 0.00070 USD   [oai_citation_attribution:0‡Investing.com](https://www.investing.com/currencies/usd-krw?utm_source=chatgpt.com)
    "영국": ("GBP", 1/1800, "1원 ≈ 0.00056파운드"),    # 추정값
    "호주": ("AUD", 1/930, "1원 ≈ 0.00108달러(AUD)"),  # 1 AUD ≈ 930원  [oai_citation_attribution:1‡xe.com](https://www.xe.com/currencyconverter/convert/?Amount=1&From=AUD&To=KRW&utm_source=chatgpt.com)
    "베트남": ("VND", 18.86, "1원 ≈ 18.86동"),        # 1원 ≈ 18.86 VND  [oai_citation_attribution:2‡환율 교환소](https://www.exchange-rates.org/exchange-rate-history/vnd-krw?utm_source=chatgpt.com)
    "인도네시아": ("IDR", 11.56, "1원 ≈ 11.56루피아"), # 1 KRW ≈ 11.56 IDR  [oai_citation_attribution:3‡xe.com](https://www.xe.com/currencyconverter/convert/?Amount=1&From=IDR&To=KRW&utm_source=chatgpt.com)
}

# --- 여행 일정표 입력 기능 ---
st.subheader("📆 여행 일정 입력")
departure = st.date_input("출국일", datetime.date.today())
return_date = st.date_input("귀국일", datetime.date.today() + datetime.timedelta(days=7))
if return_date < departure:
    st.error("⚠️ 귀국일이 출국일보다 앞설 수 없습니다.")
else:
    duration = (return_date - departure).days
    st.write(f"➡️ 여행 기간: **{duration}일**")

st.markdown("---")

# --- 세션 상태 초기화 ---
if "travel_history" not in st.session_state:
    st.session_state.travel_history = []
if "checklist" not in st.session_state:
    st.session_state.checklist = {}
if "report_on" not in st.session_state:
    st.session_state.report_on = False

# --- 국가/도시 선택 ---
col_country, col_city = st.columns(2)
with col_country:
    country = st.selectbox("🌍 국가 선택", list(safety_data.keys()))
with col_city:
    city = st.selectbox("🏙️ 도시 선택", safety_data[country]["도시"])

if st.button("🔍 안전 보고서 보기", type="primary"):
    st.session_state.travel_history.append({
        "국가": country,
        "도시": city,
        "출국일": departure,
        "귀국일": return_date
    })
    if country not in st.session_state.checklist:
        st.session_state.checklist[country] = {
            item: False for item in ["여권/비자 확인", "보험 가입", "비상연락망 저장", "신용카드 분실 신고처 메모"]
        }
    st.session_state.selected_country = country
    st.session_state.selected_city = city
    st.session_state.report_on = True
    st.rerun()

# --- 보고서 표시 ---
if st.session_state.report_on:
    sel_country = st.session_state.selected_country
    sel_city = st.session_state.selected_city
    info = safety_data[sel_country]

    st.header(f"📋 {sel_country} – {sel_city} 안전 보고서")

    # 긴급 전화 링크
    phone = info["현지 연락처"]["긴급 전화"].split(" / ")[0]
    st.markdown(f"[📞 긴급전화 걸기](tel:{phone})")

    # 환율 표시
    if sel_country in exchange_rates:
        code, rate, text = exchange_rates[sel_country]
        st.metric("💱 환율", text)

    st.markdown("---")

    # 지도 표시
    coords = {
        "서울": (37.5665, 126.9780),
        "부산": (35.1796, 129.0756),
        "제주": (33.4996, 126.5312),
        "인천": (37.4563, 126.7052),
        "대구": (35.8714, 128.6014),
        "광주": (35.1595, 126.8526),
        "울산": (35.5384, 129.3160),
        "도쿄": (35.6895, 139.6917),
        "오사카": (34.6937, 135.5023),
        "후쿠오카": (33.5904, 130.4017),
        "삿포로": (43.0618, 141.3545),
        "교토": (35.0116, 135.7681),
        "요코하마": (35.4437, 139.6380),
        "나고야": (35.1815, 136.9066),
        "방콕": (13.7563, 100.5018),
        "푸켓": (7.9519, 98.3381),
        "치앙마이": (18.7883, 98.9853),
        "파타야": (12.9236, 100.8825),
        "끄라비": (8.0350, 98.9063),
        "코사무이": (9.5120, 100.0134),
        "프놈펜": (11.5564, 104.9282),
        "시엠립": (13.3633, 103.8618),
        "시아누크빌": (10.6260, 103.5130),
        "앙코르": (13.4125, 103.8667),
        "바탐방": (13.1000, 103.2000),
        "뉴욕": (40.7128, -74.0060),
        "LA": (34.0522, -118.2437),
        "샌프란시스코": (37.7749, -122.4194),
        "하와이": (21.3069, -157.8583),
        "시카고": (41.8781, -87.6298),
        "런던": (51.5074, -0.1278),
        "맨체스터": (53.4808, -2.2426),
        "에든버러": (55.9533, -3.1883),
        "리버풀": (53.4084, -2.9916),
        "시드니": (33.8688, 151.2093),
        "멜버른": (37.8136, 144.9631),
        "브리즈번": (-27.4698, 153.0251),
        "퍼스": (-31.9505, 115.8605),
        "하노이": (21.0278, 105.8342),
        "호찌민": (10.8231, 106.6297),
        "다낭": (16.0544, 108.2022),
        "나트랑": (12.2388, 109.1967),
        "발리": (-8.3405, 115.0920),
        "자카르타": (-6.2088, 106.8456),
        "롬복": (-8.4095, 116.1572),
        "욕야카르타": (-7.7956, 110.3695),
    }
    lat, lon = coords.get(sel_city, (0, 0))
    st.subheader("📍 여행지 지도 조회")
    st.map(pd.DataFrame({"lat":[lat], "lon":[lon]}))

    st.markdown("---")

    st.subheader("⚠️ 주요 위험 및 유의사항")
    for r in info["위험 정보"]:
        st.warning(r)

    st.subheader("✅ 대처 요령")
    for t in info["대처 요령"]:
        st.success(t)

    st.subheader("📰 최근 위험 이슈")
    for issue in info.get("추가 이슈", []):
        st.info(issue)

    st.markdown("---")

    st.subheader("🧳 여행 전 필수 점검")
    checklist = st.session_state.checklist[sel_country]
    for item in checklist.keys():
        checklist[item] = st.checkbox(item, checklist[item], key=f"{sel_country}_{item}")
    done = sum(checklist.values())
    total = len(checklist)
    if done < total:
        st.warning(f"⚠️ {done}/{total} 항목 완료 — 출국 전 추가 점검 필요")
    else:
        st.success("🎉 모든 준비 완료! 안전한 여행 되세요.")

    st.markdown("---")

# --- 여행 기록 테이블 ---
st.subheader("📜 나의 여행 기록")
if st.session_state.travel_history:
    st.dataframe(pd.DataFrame(st.session_state.travel_history))
else:
    st.info("아직 여행 기록이 없습니다.")
