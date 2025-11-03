# 파일명: safetrip_v10_tabbed_final_rate_separated_modified_v4_emergency_embassy_hospital_added.py
import streamlit as st
import pandas as pd
import datetime
import pydeck as pdk

# --- 다국어 문자열 사전 (V10 기반) ---
translations = {
    "ko": {
        "title": "✈️ SafeTrip",
        "caption": "여행 일정표 · 지도 · 최신 이슈 · 긴급전화 링크 · 확대 국가/도시 정보 포함",
        "lang_select": "언어 선택",
        "travel_schedule": "📆 여행 일정 입력",
        "departure": "출국일",
        "return": "귀국일",
        "duration_prefix": "➡️ 여행 기간: ",
        "days_suffix": "일",
        "country_select": "🌍 국가 선택",
        "city_select": "🏙️ 도시 선택",
        "search_report": "🔍 안전 보고서 보기",
        "emergency_section": "🚨 응급 상황 대처",
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
    },
    "en": {
        "title": "✈️ SafeTrip Full Version (v10) - Tab & Search Integrated",
        "caption": "Travel schedule · Map · Latest issues · Emergency call link · Expanded countries/cities info",
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
    }
}

# --------------------------------------------------------------------------------
# 💡 추가: 국가별 대사관 및 병원 정보
# --------------------------------------------------------------------------------
embassy_hospital_data = {
    "일본": {
        "대사관": "Embassy of the Republic of Korea in Japan +81-3-3452-7611",
        "병원": ["Tokyo Metropolitan Hiroo Hospital (도쿄)", "Osaka University Hospital (오사카)"]
    },
    "태국": {
        "대사관": "Embassy of the Republic of Korea in Thailand +66-2-247-7537",
        "병원": ["Bumrungrad International Hospital (방콕)", "Bangkok Hospital (방콕)"]
    },
    "미국": {
        "대사관": "Embassy of the Republic of Korea in the USA +1-202-939-5600",
        "병원": ["NewYork-Presbyterian Hospital (뉴욕)", "UCLA Medical Center (LA)"]
    },
    "영국": {
        "대사관": "Embassy of the Republic of Korea in the UK +44-20-7227-5500",
        "병원": ["St Thomas' Hospital (런던)", "Manchester Royal Infirmary (맨체스터)"]
    },
    "호주": {
        "대사관": "Embassy of the Republic of Korea in Australia +61-2-6270-4100",
        "병원": ["Royal Prince Alfred Hospital (시드니)", "The Alfred Hospital (멜버른)"]
    },
    "베트남": {
        "대사관": "Embassy of the Republic of Korea in Vietnam +84-24-3831-5110",
        "병원": ["Vinmec International Hospital (하노이)", "FV Hospital (호찌민)"]
    },
    "캄보디아": {
        "대사관": "Embassy of the Republic of Korea in Cambodia +855-23-211-912",
        "병원": ["Royal Phnom Penh Hospital (프놈펜)", "Angkor Hospital for Children (시엠립)"]
    },
    "인도네시아": {
        "대사관": "Embassy of the Republic of Korea in Indonesia +62-21-2967-2555",
        "병원": ["Siloam Hospitals (자카르타)", "BIMC Hospital (발리)"]
    },
}

# --------------------------------------------------------------------------------
# (이 아래로는 기존 safetrip_v10 코드 전부 동일)
# --------------------------------------------------------------------------------

# ⚠️ 생략된 기존 코드 부분은 그대로 유지됨 — 여행 일정, 도시 선택, 환율, 지도 등 전부 동일

# 응급상황 대처 탭 부분만 수정
with tab4:
    st.subheader(_["emergency_section"])
    phone_raw = info["현지 연락처"]["긴급 전화"]
    phone = phone_raw.split(" / ")[0]

    st.markdown("### 🚨 " + (_["emergency_section"].split(" ")[-1] if lang=="ko" else "Local Emergency Number"))
    st.error(f"**{phone_raw}**")
    st.markdown(f"[{_['call_emergency']}](tel:{phone})")

    # 🏛️ 대사관 연락처 표시
    st.markdown("---")
    st.markdown("### 🏛️ 대사관 연락처")
    embassy_info = embassy_hospital_data.get(sel_country_ko, {}).get("대사관", "정보 없음 / No Info")
    st.write(embassy_info)

    # 🏥 주요 병원 정보 표시
    st.markdown("---")
    st.markdown("### 🏥 주요 병원 정보")
    hospitals = embassy_hospital_data.get(sel_country_ko, {}).get("병원", [])
    if hospitals:
        for h in hospitals:
            st.write(f"- {h}")
    else:
        st.write("정보 없음 / No Info")

    # 기존 설명 및 검색 버튼 유지
    st.markdown("---")
    info_text = (
        "💡 **국가별 맞춤 대처 정보:** 긴급 전화는 **1차적인 연결** 수단입니다. 상황별 상세 대처법은 아래 검색을 통해 확인하세요."
        if lang == "ko"
        else "💡 **Country-specific Response Info:** Emergency call is the **primary connection** method. Check detailed response tips below."
    )
    st.info(info_text)

    st.markdown("#### ⚠️ " + (_["risk_info"].split(" ")[-2] if lang=="ko" else "Key Risks Reference"))
    for r in risks:
        st.warning(f"• {r}")

    st.markdown("---")
    current_search_query = f"{sel_country_display} 여행 긴급 상황 대처"
    st.link_button(
        f"🚨 **{sel_country_display}** " + (_["emergency_section"].split(" ")[-1] if lang=="ko" else "Detailed Emergency Response") + f": {_['search_link_btn']}",
        create_google_search_link(current_search_query),
        use_container_width=True
    )
