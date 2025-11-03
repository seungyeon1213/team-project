# 파일명: safetrip_v11_emergency_improved_localphrases_mapadded.py
import streamlit as st
import pandas as pd
import datetime
import pydeck as pdk

# --- 다국어 문자열 사전 ---
translations = {
    "ko": {
        "title": "✈️ SafeTrip",
        "caption": "여행 일정표 · 지도 · 최신 이슈 · 긴급전화 링크 · 대사관/병원 정보 포함",
        "lang_select": "언어 선택",
        "travel_schedule": "📆 여행 일정 입력",
        "departure": "출국일",
        "return": "귀국일",
        "duration_prefix": "➡️ 여행 기간: ",
        "days_suffix": "일",
        "country_select": "🌍 국가 선택",
        "city_select": "🏙️ 도시 선택",
        "search_report": "🔍 안전 보고서 보기",
        "emergency_section": "🚨 긴급 상황 대처",
        "call_emergency": "📞 긴급전화 걸기",
        "risk_info": "⚠️ 주요 위험 및 유의사항",
        "tips_info": "✅ 대처 요령",
        "recent_issues": "📰 최근 위험 이슈",
        "checklist_section": "🧳 여행 전 필수 점검",
        "record_section": "📜 나의 여행 기록",
        "complete_success": "🎉 모든 준비 완료! 안전한 여행 되세요.",
        "search_link_btn": "구글에서 더 알아보기",
        "exchange_rate": "💱 환율 정보",
        "map_section": "🗺️ 도시 지도",
        "embassy_contact": "🏛️ 대사관 연락처",
        "major_hospitals": "🏥 주요 병원 정보",
        "local_phrases": "🗣️ 현지어 응급 문장",
        "phrase_help": "도와주세요",
        "phrase_hospital": "병원",
    },
    "en": {
        "title": "✈️ SafeTrip (v11 Enhanced Emergency)",
        "caption": "Travel schedule · Map · Issues · Emergency call · Embassy/Hospital info included",
        "lang_select": "Select Language",
        "travel_schedule": "📆 Enter Travel Schedule",
        "departure": "Departure Date",
        "return": "Return Date",
        "duration_prefix": "➡️ Trip Duration: ",
        "days_suffix": " days",
        "country_select": "🌍 Select Country",
        "city_select": "🏙️ Select City",
        "search_report": "🔍 View Safety Report",
        "emergency_section": "🚨 Emergency Response",
        "call_emergency": "📞 Make Emergency Call",
        "risk_info": "⚠️ Key Risks & Notices",
        "tips_info": "✅ Response Tips",
        "recent_issues": "📰 Recent Issues",
        "checklist_section": "🧳 Pre-Travel Checklist",
        "record_section": "📜 My Travel Records",
        "complete_success": "🎉 All set! Have a safe trip.",
        "search_link_btn": "Search on Google",
        "exchange_rate": "💱 Exchange Rate Info",
        "map_section": "🗺️ City Map",
        "embassy_contact": "🏛️ Embassy Contact",
        "major_hospitals": "🏥 Major Hospitals",
        "local_phrases": "🗣️ Local Emergency Phrases",
        "phrase_help": "I need help",
        "phrase_hospital": "hospital",
    }
}

# --- 기존 safety_data 등 그대로 ---
# (여기서는 요약 생략, 원래 코드 그대로 유지)

# --- 예시로 현지어 응급 문장 추가 ---
local_emergency_phrases = {
    "일본": {"도와주세요": "助けてください", "병원": "病院"},
    "태국": {"도와주세요": "ช่วยด้วย", "병원": "โรงพยาบาล"},
    "캄보디아": {"도와주세요": "សូមជួយខ្ញុំ", "병원": "មន្ទីរពេទ្យ"},
    "미국": {"도와주세요": "Help me", "병원": "Hospital"},
    "영국": {"도와주세요": "Help me", "병원": "Hospital"},
    "호주": {"도와주세요": "Help me", "병원": "Hospital"},
    "베트남": {"도와주세요": "Giúp tôi", "병원": "Bệnh viện"},
    "인도네시아": {"도와주세요": "Tolong saya", "병원": "Rumah sakit"},
    "한국": {"도와주세요": "도와주세요", "병원": "병원"},
}

# --- 대사관/병원 정보 샘플 추가 ---
emergency_facilities = {
    "일본": {
        "대사관": "주일 대한민국 대사관 (도쿄)",
        "병원": "세인트 루크 국제병원 (Tokyo)",
    },
    "태국": {
        "대사관": "주태국 대한민국 대사관 (Bangkok)",
        "병원": "Bumrungrad International Hospital (Bangkok)",
    },
    "미국": {
        "대사관": "주미 대한민국 대사관 (Washington D.C.)",
        "병원": "NewYork-Presbyterian Hospital",
    },
    "호주": {
        "대사관": "주호주 대한민국 대사관 (Canberra)",
        "병원": "Royal Prince Alfred Hospital (Sydney)",
    },
}

# --- 기존 함수들 그대로 유지 (생략) ---
# translate_name, get_country_name_list, get_city_name_list 등 동일

# ------------------------------------------------------------------------------------------------------
# Streamlit 시작 (기존과 동일)
# ------------------------------------------------------------------------------------------------------

lang_option = st.selectbox(translations["ko"]["lang_select"], ("한국어", "English"))
lang = "ko" if lang_option == "한국어" else "en"
_ = translations[lang]
st.set_page_config(page_title=_["title"], page_icon="✈️", layout="wide")

st.title(_["title"])
st.caption(_["caption"])
st.markdown("---")

# ... (여행 일정, 국가 선택, 보고서 버튼 등 기존 동일 코드)

# --- 보고서 표시 ---
if st.session_state.get("report_on", False):
    sel_country_ko = st.session_state.selected_country_ko
    sel_city_ko = st.session_state.selected_city_ko
    sel_country_display = sel_country_ko
    sel_city_display = sel_city_ko

    st.header(f"📋 {sel_country_display} – {sel_city_display}")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        _["risk_info"], _["tips_info"], _["recent_issues"],
        _["emergency_section"], _["checklist_section"]
    ])

    # -------------------------------------------------------------
    # ✅ 개선된 응급상황 탭
    # -------------------------------------------------------------
    with tab4:
        st.subheader(_["emergency_section"])

        phone_raw = safety_data[sel_country_ko]["현지 연락처"]["긴급 전화"]
        phone = phone_raw.split(" / ")[0]

        st.error(f"**{_['call_emergency']}: {phone_raw}**")
        st.markdown(f"[{_['call_emergency']}](tel:{phone})")

        st.markdown("---")
        st.markdown(f"### {_['embassy_contact']}")
        embassy = emergency_facilities.get(sel_country_ko, {}).get("대사관", "정보 없음 / No Info")
        st.info(embassy)

        st.markdown(f"### {_['major_hospitals']}")
        hospital = emergency_facilities.get(sel_country_ko, {}).get("병원", "정보 없음 / No Info")
        st.info(hospital)

        st.markdown(f"### {_['local_phrases']}")
        phrases = local_emergency_phrases.get(sel_country_ko, {})
        st.write(f"- {_['phrase_help']}: `{phrases.get('도와주세요', '-')}`")
        st.write(f"- {_['phrase_hospital']}: `{phrases.get('병원', '-')}`")

        st.markdown("---")
        st.link_button(
            f"🚨 {sel_country_display} {_['search_link_btn']}",
            f"https://www.google.com/search?q={sel_country_display}+여행+긴급상황+대처",
            use_container_width=True
        )

    # -------------------------------------------------------------
    # ✅ 지도에 응급시설 마커 추가
    # -------------------------------------------------------------
    st.markdown("---")
    st.subheader(_["map_section"])

    lat, lon = (coords.get(sel_city_ko, (0, 0)))
    data_points = [
        {"name": sel_city_display, "lat": lat, "lon": lon, "color": [0, 128, 255]},
    ]
    if sel_country_ko in emergency_facilities:
        data_points.append({"name": "Embassy", "lat": lat + 0.01, "lon": lon + 0.01, "color": [255, 0, 0]})
        data_points.append({"name": "Hospital", "lat": lat - 0.01, "lon": lon - 0.01, "color": [0, 255, 0]})

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data_points,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius=70000,
        pickable=True,
    )
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=6)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}"}))

    # (이하 기존 체크리스트, 기록표 등 동일)
