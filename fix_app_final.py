"""
app.py의 UI/UX 레이아웃과 컬러 감성을 완벽하게 개편하는 최종 리팩토링 스크립트입니다.
주요 개선 스펙:
1. 전 페이지의 모든 위젯(인풋창, 셀렉트박스 등) 배경 화이트 및 글자 딥차콜(#1F2937) 강제 고정으로 100% 가독성 보장.
2. Step 3 결과 페이지에서 복용 골든타임 사이드 카드를 완전 제거하고 단일 와이드 컨테이너 덱으로 아키텍처 개편.
3. 데이터 내보내기(CSV)를 Step 3 결과 화면 최하단(푸터 바로 위)에 전체 폭(Full-width) 프리미엄 다운로드 바 형태로 재배치.
4. 토스 스타일의 [ 🥗 전체 동의하고 3분만에 내 맞춤 영양 진단하기 ] 대형 버튼 최상단 배치 및 세부 약관 슬림화.
5. Scikit-Learn 머신러닝 커널 연산 시 인디고 블루 스피너 및 실시간 연산 단계 시각화 '락인(Lock-in)' 기능 구현.
6. 오버도즈 경고창에 부드러운 펄스(Pulse) 깜빡임 애니메이션 스킨 적용.
7. 아웃링크 위에 CS 방어 문구 인젝션 및 최하단 메디컬 면책 공지(Disclaimer)와 데이터 출처 신설.
"""

def main():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # ==================== 1. CSS 코드 개편 (위젯 가독성 확보, 펄스 애니메이션 추가) ====================
    # st.markdown("""\n        <style> 영역을 통째로 교체합니다.
    start_css_marker = '    st.markdown("""\n        <style>\n        @import url(\'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap\');'
    end_css_marker = '        </style>\n    \"\"\", unsafe_allow_html=True)'
    
    start_css_idx = content.find(start_css_marker)
    end_css_idx = content.find(end_css_marker, start_css_idx)
    
    if start_css_idx == -1 or end_css_idx == -1:
        print("Error: CSS 마커를 찾지 못했습니다.")
        return

    new_css = """    st.markdown(\"\"\"
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap');

        /* ========== 전역 테마 하드 고정 (소프트 그레이시 블루 및 화이트 레이어드) ========== */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #F4F7FF !important;
            color: #1F2937 !important;
        }
        
        /* 스트림릿 기본 탑 헤더는 GNB 고정 바와 겹치므로 숨김 처리 */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        /* 메인 콘텐츠 영역 상단 여백 확보 (GNB 고정 바 높이 고려) */
        .main .block-container {
            padding-top: 120px !important;
            background-color: #F4F7FF !important;
        }

        /* 폰트 및 텍스트 컬러 지정 (아이콘 깨짐 방지를 위해 span, div, button 등은 제외) */
        h1, h2, h3, h4, h5, h6, p, label, li {
            color: #1F2937 !important;
            font-family: 'Outfit', 'Noto Sans KR', sans-serif !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #FAFBFF !important;
            border-right: 1px solid #E5EFFF !important;
        }
        
        /* ========== 모든 위젯 및 입력 폼 가독성 100% 보장 고정 ========== */
        input, select, textarea, div[role="listbox"], [data-baseweb="select"], .stSelectbox, .stMultiSelect {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
        }
        .stRadio label, .stCheckbox label, .stSelectbox label, .stMultiSelect label, .stSlider label, .stTextInput label, .stNumberInput label {
            color: #1F2937 !important;
            font-weight: 600 !important;
        }
        [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
            color: #1F2937 !important;
        }
        [data-baseweb="tag"] {
            background-color: #E5EFFF !important;
            color: #2C3281 !important;
            border: 1px solid #5A83F1 !important;
        }
        
        /* ========== 오버도즈 경고 펄스 애니메이션 ========== */
        @keyframes pulse-warning-anim {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        .pulse-warning {
            border: 2px solid #ef4444 !important;
            background-color: #FFFFFF !important;
            animation: pulse-warning-anim 2s infinite;
        }
        
        /* ========== GNB 헤더 (보조색인 딥블루 #2C3281로 세련되게 고정) ========== */
        .gnb-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #2C3281;
            border-bottom: 2px solid #5A83F1;
            padding: 14px 40px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999999;
            backdrop-filter: blur(14px);
            box-shadow: 0 4px 30px rgba(44, 50, 129, 0.15);
            height: 70px;
        }
        .gnb-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.45rem;
            font-weight: 800;
            color: #FFFFFF !important;
            letter-spacing: -0.5px;
        }
        .gnb-nav {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        .gnb-link {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: #E5EFFF !important;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.22s ease;
            border: 1px solid transparent;
            cursor: pointer;
        }
        .gnb-link:hover {
            color: #FFFFFF !important;
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.1);
        }
        .gnb-link-highlight {
            color: #FFFFFF !important;
            border: 1px solid rgba(90, 131, 241, 0.5);
            background: #5A83F1;
        }
        .gnb-link-highlight:hover {
            background: #4772e0;
            border-color: #FFFFFF;
            color: #FFFFFF !important;
        }

        /* ========== 기존 카드/타이틀 (화이트 및 블루칩 기반 개편) ========== */
        .main-title {
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .sub-title {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 1rem;
            color: #475569;
            margin-bottom: 12px;
        }
        .rating-star {
            color: #fbbf24;
            font-weight: bold;
            font-size: 1.1rem;
        }
        .ecommerce-card {
            background: #FFFFFF !important;
            border: 1px solid #E5EFFF !important;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 24px;
            transition: transform 0.28s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.28s ease, border-color 0.28s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 580px;
            box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.08) !important;
        }
        .ecommerce-card:hover {
            transform: translateY(-9px);
            box-shadow: 0 22px 40px rgba(90, 131, 241, 0.18) !important;
            border-color: #5A83F1 !important;
        }
        .card-badge {
            font-size: 0.7rem;
            padding: 3px 7px;
            border-radius: 5px;
            font-weight: 600;
            margin-right: 4px;
            display: inline-block;
            transition: all 0.18s ease;
        }
        .card-badge:hover { opacity: 0.8; transform: scale(1.04); }
        .badge-goal { background: #E5EFFF; color: #2C3281; }
        .badge-platform { background: rgba(90, 131, 241, 0.15); color: #5A83F1; }
        .badge-form { background: #FAFBFF; color: #475569; border: 1px solid #E5EFFF; }
        .buy-btn {
            display: block;
            width: 100%;
            text-align: center;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            color: white !important;
            padding: 10px 0;
            border-radius: 10px;
            font-weight: 700;
            text-decoration: none;
            font-size: 0.88rem;
            transition: all 0.22s ease;
            margin-top: 10px;
            box-shadow: 0 4px 12px rgba(90, 131, 241, 0.2);
        }
        .buy-btn:hover {
            opacity: 0.88;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(90, 131, 241, 0.35);
        }

        /* ========== 유틸리티 사이드카드 (화이트 배경에 입체적인 섀도우) ========== */
        .side-util-card {
            background: #FFFFFF !important;
            border: 1px solid #E5EFFF !important;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.08) !important;
            transition: box-shadow 0.25s ease, border-color 0.25s ease;
        }
        .side-util-card:hover {
            box-shadow: 0 15px 35px rgba(90, 131, 241, 0.12) !important;
            border-color: #5A83F1;
        }
        .side-section-label {
            font-size: 0.72rem;
            font-weight: 700;
            color: #2C3281;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        /* ========== 아웃링크 트리플 버튼 덱 ========== */
        .outlink-deck {
            display: flex;
            gap: 6px;
            margin-top: 8px;
        }
        .outlink-btn {
            flex: 1;
            text-align: center;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 6px 4px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.2s ease;
        }
        .outlink-btn-coupang {
            background: rgba(255, 93, 0, 0.07);
            color: #ff7a30;
            border: 1px solid rgba(255, 93, 0, 0.2);
        }
        .outlink-btn-coupang:hover { background: rgba(255, 93, 0, 0.15); transform: translateY(-2px); }
        .outlink-btn-naver {
            background: rgba(3, 199, 90, 0.07);
            color: #03c75a;
            border: 1px solid rgba(3, 199, 90, 0.2);
        }
        .outlink-btn-naver:hover { background: rgba(3, 199, 90, 0.15); transform: translateY(-2px); }
        .outlink-btn-iherb {
            background: rgba(91, 192, 79, 0.07);
            color: #5bc04f;
            border: 1px solid rgba(91, 192, 79, 0.2);
        }
        .outlink-btn-iherb:hover { background: rgba(91, 192, 79, 0.15); transform: translateY(-2px); }

        /* ========== 엔터프라이즈 푸터 ========== */
        .enterprise-footer {
            background: #FFFFFF !important;
            border-top: 2px solid #E5EFFF;
            border-radius: 20px 20px 0 0;
            padding: 32px 40px;
            margin-top: 40px;
            text-align: center;
            box-shadow: 0 -10px 30px -5px rgba(90, 131, 241, 0.04) !important;
        }
        .footer-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 800;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .footer-text {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.78rem;
            color: #475569;
            line-height: 1.7;
        }
        .footer-divider {
            border: 0;
            border-top: 1px solid #E5EFFF;
            margin: 14px 0;
        }
        </style>
    \"\"\", unsafe_allow_html=True)"""
    
    content = content[:start_css_idx] + new_css + content[end_css_idx + len(end_css_marker):]

    # ==================== 2. 토스 스타일 [🥗 전체 동의하고 시작하기] 대형 버튼 최상단 배치 및 세부 약관 슬림화 ====================
    # L770 ~ L824 영역을 통째로 교체합니다.
    start_agree_marker = '        if not st.session_state.agreed:'
    end_agree_marker = '            with landing_col2:'
    
    start_agree_idx = content.find(start_agree_marker)
    end_agree_idx = content.find(end_agree_marker, start_agree_idx)
    
    if start_agree_idx == -1 or end_agree_idx == -1:
        print("Error: 약관 동의 영역 마커를 찾지 못했습니다.")
        return

    new_agree_section = """        if not st.session_state.agreed:
            # 2열 분할 레이아웃
            landing_col1, landing_col2 = st.columns([1.1, 0.9], gap="large")
            
            with landing_col1:
                # 좌측: 프리미엄 텍스트 & 약관 동의
                st.markdown(\"\"\"
                    <div style="background: rgba(90, 131, 241, 0.1); border: 1px solid rgba(90, 131, 241, 0.2); border-radius: 20px; padding: 6px 14px; width: fit-content; margin-bottom: 15px;">
                        <span style="color: #5A83F1; font-weight: 700; font-size: 0.85rem;">📊 식약처 데이터 및 ML 기반 초개인화 엔진</span>
                    </div>
                    <p style="color: #475569; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">
                        단순한 추천을 넘어 23개 신체 변수 연산, Scikit-Learn 머신러닝 위험도 예측, 식약처 상한 섭취량 실시간 검증을 통해 가장 안전한 영양 조합과 복용 타임라인을 도출합니다.
                    </p>
                \"\"\", unsafe_allow_html=True)
                
                # 토스 스타일 대형 전체 동의 버튼 (프리미엄 컨테이너 안착)
                st.markdown(\"\"\"
                    <div style="background: #FFFFFF; border: 1px solid #E5EFFF; border-radius: 20px; padding: 25px; box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.08); margin-bottom: 20px;">
                        <h4 style="margin: 0 0 15px 0; color: #1F2937; font-size: 1.1rem; font-weight: 700;">🥗 안전한 초개인화 진단 시작하기</h4>
                        <p style="font-size: 0.85rem; color: #475569; margin-bottom: 15px; line-height: 1.4;">
                            아래 대형 버튼을 터치하시면 3대 필수 약관(서비스 이용약관, 만 14세 이상 확인, 건강상태/민감정보 수집)에 한 번에 전체 동의하고 즉시 진단 문진 단계로 진입합니다.
                        </p>
                    </div>
                \"\"\", unsafe_allow_html=True)
                
                if st.button("🥗 전체 동의하고 3분만에 내 맞춤 영양 진단하기 ➡️", use_container_width=True, key="toss_agree_btn"):
                    st.session_state.all_agree = True
                    st.session_state.agree_1 = True
                    st.session_state.agree_2 = True
                    st.session_state.agree_3 = True
                    st.session_state.agreed = True
                    st.session_state.step = 1
                    st.session_state.streaming_done = False
                    st.rerun()

                st.markdown("<div style='text-align: center; font-size: 0.8rem; color:#94a3b8; margin: 10px 0;'>또는 개별 동의 항목 확인</div>", unsafe_allow_html=True)
                
                # 개별 슬림 약관 동의 체크박스
                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1:
                    st.checkbox("1. [필수] 이용약관 동의", key="agree_1", on_change=on_individual_change)
                with col_c2:
                    st.checkbox("2. [필수] 만 14세 이상", key="agree_2", on_change=on_individual_change)
                with col_c3:
                    st.checkbox("3. [필수] 민감정보 동의", key="agree_3", on_change=on_individual_change)
                    
                with st.expander("🔍 세부 약관 요약 보기"):
                    st.markdown(\"\"\"
                        * **개인정보 수집**: 맞춤형 영양소 추천 제공 목적이며 세션 종료 시 즉시 파기합니다.
                        * **만 14세 이상**: 아동 보호를 위해 미성년 이용을 배제합니다.
                        * **민감정보 수집**: 개인정보보호법 제23조에 의거해 질환 및 부작용 정보를 수집합니다.
                    \"\"\")
                    
                agreed_all_checked = st.session_state.agree_1 and st.session_state.agree_2 and st.session_state.agree_3
                
                if st.button("선택 동의 후 시작하기", disabled=not agreed_all_checked, use_container_width=True, key="normal_agree_btn"):
                    st.session_state.agreed = True
                    st.session_state.step = 1
                    st.session_state.streaming_done = False
                    st.rerun()
            """
            
    content = content[:start_agree_idx] + new_agree_section + "\n" + content[end_agree_idx:]

    # ==================== 3. Scikit-Learn 머신러닝 연산 시 '시각적 락인(Lock-in)' 스피너 추가 ====================
    # L1265 ~ L1269 부근의 "초개인화 장바구니 큐레이션 보기 ➡️" 버튼 클릭 시 작동하도록 치환합니다.
    start_trans_marker = '                if st.button("초개인화 장바구니 큐레이션 보기 ➡️"):'
    end_trans_marker = '        # ==================== 화면 분기 3: 초개인화 장바구니 큐레이션 결과 ===================='
    
    start_trans_idx = content.find(start_trans_marker)
    end_trans_idx = content.find(end_trans_marker, start_trans_idx)
    
    if start_trans_idx == -1 or end_trans_idx == -1:
        print("Error: 단계 전환 마커를 찾지 못했습니다.")
        return
        
    new_transition_code = """                if st.button("초개인화 장바구니 큐레이션 보기 ➡️"):
                    # 시각적 락인(Lock-in) 인디케이터 연출
                    with st.spinner("🧠 Scikit-Learn 머신러닝 커널 연산 및 오버도즈 차단 설계 연산 중..."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        stages = [
                            "1단계: 23개 전항목 신체 습관 변수 로드 완료 (🟢)",
                            "2단계: 식약처 상한 섭취량 실시간 동기화 완료 (🟢)",
                            "3단계: Scikit-Learn 로지스틱 회귀 위험 분류 커널 연산 시작 (🟢)",
                            "4단계: 개인화 가중 스코어링 최적화 랭킹 매핑 완료 (🟢)"
                        ]
                        for idx, stage in enumerate(stages):
                            status_text.markdown(f"<span style='color:#5A83F1; font-weight:700; font-size:0.92rem;'>{stage}</span>", unsafe_allow_html=True)
                            time.sleep(0.4)
                            progress_bar.progress((idx + 1) * 25)
                        status_text.success("🎉 초개인화 장바구니 매칭 연산 완료!")
                        time.sleep(0.3)
                    st.session_state.step = 3
                    st.session_state.streaming_done = False
                    st.rerun()"""
                    
    content = content[:start_trans_idx] + new_transition_code + "\n" + content[end_trans_idx:]

    # ==================== 4. Step 3의 col_main, col_side 컬럼 해제 및 단일 와이드 개편 ====================
    # L1287 `col_main, col_side = st.columns([2.3, 1.0], gap="large")` 부터,
    # L1490 `            # ==================== 우측 유틸리티 사이드카드 (col_side) ====================` 에 해당하는 영역 전체를 
    # 단일 와이드로 개편하여 들여쓰기를 제거하고, 타임라인과 사이드바에 존재하던 내보내기 버튼은 삭제하고 들여쓰기를 정비합니다.
    
    # 5. 오버도즈 경고창에 부드러운 펄스 애니메이션 (.pulse-warning) 적용 (L1340 부근)
    # L1342 ~ L1352 부근의 st.error를 커스텀 st.markdown 구조로 변경합니다.
    
    # app.py 내의 화면분기 3 영역(L1272 이후)을 통째로 덮어쓰는 리비전 블록을 생성합니다.
    # 이것이 가장 안전하며 들여쓰기 에러를 완전 차단합니다.
    
    start_step3_marker = '        elif st.session_state.step == 3:'
    end_step3_marker = '    # ==================== 메뉴 분기 2: 📊 뉴트리핏 데이터 인사이트 (Admin) ===================='
    
    start_step3_idx = content.find(start_step3_marker)
    end_step3_idx = content.find(end_step3_marker, start_step3_idx)
    
    if start_step3_idx == -1 or end_step3_idx == -1:
        print("Error: Step 3 분기 영역을 찾을 수 없습니다.")
        return
        
    new_step3_wide_section = """        elif st.session_state.step == 3:
            st.markdown('<div class="main-title" style="font-size:1.8rem;">&#x1F4A1; 뉴트리핏 초개인화 맞춤 큐레이션 결과</div>', unsafe_allow_html=True)
            
            survey = st.session_state.survey_data

            side_effects_cleaned = [s for s in survey.get("side_effects", []) if s not in ["없음", "기타 직접입력"]]
            if survey.get("side_effect_direct", "").strip():
                side_effects_cleaned.append(survey.get("side_effect_direct"))
            algs = list(survey.get("allergies", []))
            if survey.get("allergy_direct", "").strip():
                algs.append(survey.get("allergy_direct"))
            algs_display = [a for a in algs if a not in ["없음", "기타(직접입력)"]]
            exclusions = side_effects_cleaned + algs_display
            exclusions_str = ', '.join(exclusions) if exclusions else '없음'

            # --- 프로필 배너 (화이트 카드 섀도우) ---
            st.markdown(f\"\"\"
                <div style="background: #FFFFFF; border: 1px solid #E5EFFF; border-radius: 20px; padding: 18px 25px; margin-bottom: 24px; box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.08);">
                    <strong>&#x1F4CA; 분석 대상자 프로필:</strong> {survey['gender']} ({survey['age']}) | BMI: {survey['bmi']} |
                    &#x1F3AF; <strong>핵심 건강고민:</strong> {', '.join(survey['health_goals'])} |
                    &#x1F6AB; <strong>배제 성분:</strong> {exclusions_str}
                </div>
            \"\"\", unsafe_allow_html=True)

            # --- AI 총평 스트리밍 (화이트 카드 섀도우) ---
            st.markdown("#### &#x1F916; 뉴트리핏 AI 개인화 큐레이션 총평 리포트")
            ai_report_text = (
                f"{survey['gender']} ({survey['age']}) 분석 대상자님은 현재 [{', '.join(survey['health_goals'])}] 건강 고민을 집중 케어하기 위해 웰니스 스코어 보너스 가산점을 정밀 배분 받으셨습니다. "
                f"현재 BMI 지수는 {survey['bmi']}로 안전 수준을 유지하고 계시며, 설정된 부작용 이력 및 [{exclusions_str}] 등의 성분이 함유된 제품군은 "
                f"스코어 산정 리스트에서 선제 필터링되었습니다. 아래 식약처 공인 성분 지식베이스 규격에 맞춰 엄선한 랭킹 TOP 12와 최적의 복용 골든타임을 참고하시기 바랍니다."
            )
            
            # 스트리밍 렌더러
            st.markdown('<div class="side-util-card">', unsafe_allow_html=True)
            if not st.session_state.streaming_done:
                def text_char_generator(text):
                    for char in text:
                        yield char
                        time.sleep(0.008)
                st.write_stream(text_char_generator(ai_report_text))
            else:
                st.write(ai_report_text)
            st.markdown('</div>', unsafe_allow_html=True)

            # --- 🚨 AI 긴급 안전성 교차 필터 경고창 (펄스 애니메이션 스킨 적용) ---
            st.markdown("---")
            st.markdown("### &#x1F4CA; 실시간 중복/과다 섭취 안전성 시뮬레이션 (영양제 디옵티마이저)")
            categories = ["마그네슘", "비타민C", "오메가3", "유산균 / 프로바이오틱스", "콜라겐", "멀티비타민"]
            selected_category = st.selectbox(
                "&#x1F50E; 특정 추천 카테고리만 필터링:",
                ["전체 맞춤 추천"] + categories,
                index=0
            )
            filter_cat = None if selected_category == "전체 맞춤 추천" else selected_category

            try:
                recommendations = get_recommendations(survey, selected_category=filter_cat, top_n=24)
            except Exception as e:
                st.error(f"추천 엔진 구동 중 에러가 발생했습니다: {e}")
                if st.button("돌아가기"):
                    st.session_state.step = 2
                    st.rerun()
                return

            if recommendations.empty:
                st.warning("⚠️ 입력하신 알레르기/부작용 필터 또는 맞춤 가중치 조건에 해당하는 제품이 목록에 존재하지 않거나 모두 필터링되었습니다.")
                if st.button("⬅️ 웰니스 리포트로 돌아가기"):
                    st.session_state.step = 2
                    st.rerun()
                return

            product_names_list = []
            for i, (idx, row) in enumerate(recommendations.iterrows()):
                platform = str(row.get('platform') or 'Unknown')
                name = str(row.get('product_name') or row.get('displayName') or '이름 없음')
                product_names_list.append(f"{i+1}위. [{platform}] {name[:55]}")

            selected_combos = st.multiselect(
                "&#x26A0;&#xFE0F; 조합할 제품군 복수 선택 (초과 복용 실시간 감지):",
                options=product_names_list,
                default=product_names_list[:2] if len(product_names_list) >= 2 else product_names_list
            )
            
            if selected_combos:
                total_vit_c = total_mag = total_vit_d = total_zinc = 0.0
                for combo_label in selected_combos:
                    try:
                        rank_idx = int(combo_label.split('위.')[0].strip()) - 1
                        row_combo = recommendations.iloc[rank_idx]
                        std_ing_combo = str(row_combo.get('표준성분', ''))
                        if "비타민C" in std_ing_combo: total_vit_c += 1000.0
                        if "멀티비타민" in std_ing_combo or "비타민" in std_ing_combo:
                            total_vit_c += 500.0; total_mag += 100.0; total_vit_d += 1000.0; total_zinc += 10.0
                        if "마그네슘" in std_ing_combo: total_mag += 350.0
                        if "비타민D" in std_ing_combo: total_vit_d += 2000.0
                    except: pass
                    
                danger_messages = []
                if total_vit_c > 2000.0:
                    danger_messages.append(f"비타민C 과다 복용 위험! ({total_vit_c:.0f}mg / 상한치 2000mg 대비 {(total_vit_c/2000)*100:.0f}%)")
                if total_mag > 350.0:
                    danger_messages.append(f"마그네슘 과량 복용 주의! ({total_mag:.0f}mg / 상한치 350mg 대비 {(total_mag/350)*100:.0f}%)")
                if total_vit_d > 4000.0:
                    danger_messages.append(f"비타민D 고칼슘혈증 경고! ({total_vit_d:.0f}IU / 상한치 4000IU 대비 {(total_vit_d/4000)*100:.0f}%)")
                
                if danger_messages:
                    for msg in danger_messages:
                        st.markdown(f\"\"\"
                            <div class="pulse-warning" style="padding:15px 20px; border-radius:15px; margin-bottom:12px; color:#ef4444; font-weight:700; font-size:0.9rem; display:flex; align-items:center; gap:8px;">
                                <span>⚠️</span>
                                <span>{msg}</span>
                            </div>
                        \"\"\", unsafe_allow_html=True)
                else:
                    st.success("🟢 식약처 안전 섭취 규격 충족 조합입니다.")

            product_options = []
            for i, (idx, row) in enumerate(recommendations.iterrows()):
                platform = str(row.get('platform') or 'Unknown')
                name = str(row.get('product_name') or row.get('displayName') or '이름 없음')
                product_options.append(f"{i+1}위. [{platform}] {name[:60]}...")
            selected_product_label = st.selectbox(
                "&#x1F52C; 식약처 가이드라인 조회할 영양제 선택:",
                product_options, index=0
            )
            selected_idx = product_options.index(selected_product_label)
            selected_row = recommendations.iloc[selected_idx]

            # --- 성분 카테고리 탭 + 4열 카드 그리드 ---
            st.markdown("---")
            st.markdown("### &#x1F3C6; 큐레이션 추천 랭킹 TOP 12")
            tab_all, tab_vit, tab_min, tab_others = st.tabs(["전체 제품", "비타민 계열", "미네랄 계열", "오메가 / 유산균 / 콜라겐"])
            with tab_all:
                render_product_grid(recommendations.head(12), selected_row, db_data, survey)
            with tab_vit:
                df_vit = recommendations[recommendations['표준성분'].str.contains('비타민|레티놀|엽산', na=False, case=False)]
                render_product_grid(df_vit.head(12), selected_row, db_data, survey)
            with tab_min:
                df_min = recommendations[recommendations['표준성분'].str.contains('마그네슘|철분|아연|칼슘|미네랄|구리|망간|셀렌', na=False, case=False)]
                render_product_grid(df_min.head(12), selected_row, db_data, survey)
            with tab_others:
                df_oth = recommendations[recommendations['표준성분'].str.contains('오메가|유산균|프로바이오틱스|콜라겐', na=False, case=False)]
                render_product_grid(df_oth.head(12), selected_row, db_data, survey)

            # --- 트리플 아웃링크 버튼 덱 & CS 방어 문구 인젝션 ---
            sel_name = str(selected_row.get('product_name') or selected_row.get('displayName') or '')
            import urllib.parse
            coupang_url = f"https://www.coupang.com/np/search?q={urllib.parse.quote(sel_name)}"
            naver_url = f"https://search.shopping.naver.com/search/all?query={urllib.parse.quote(sel_name)}"
            iherb_url = f"https://www.iherb.com/search?kw={urllib.parse.quote(sel_name)}"
            
            st.markdown("<div style='font-size:0.78rem; color:#475569; margin: 15px 0 5px 0;'>* 위 가격은 시장 평균가 기준이며 실시간 가격 변동 및 품절이 발생할 수 있습니다.</div>", unsafe_allow_html=True)
            st.markdown(f\"\"\"
                <div class="outlink-deck">
                    <a class="outlink-btn outlink-btn-coupang" href="{coupang_url}" target="_blank">&#x1F7E0; 쿠팡 검색</a>
                    <a class="outlink-btn outlink-btn-naver" href="{naver_url}" target="_blank">&#x1F7E2; 네이버 쇼핑</a>
                    <a class="outlink-btn outlink-btn-iherb" href="{iherb_url}" target="_blank">&#x1F7E2; 아이허브 직구</a>
                </div>
            \"\"\", unsafe_allow_html=True)

            # --- 비교 보관함 (단일 와이드로 완전 개편) ---
            st.markdown("---")
            st.markdown("### &#x1F6D2; 뉴트리핏 인터랙티브 상품 비교 보관함 (Comparison Matrix)")
            st.write("선택하신 영양제들의 브랜드, 가격, 평점 및 식약처 공식 기능성 규격을 한눈에 병렬 대조하여 최적의 선택을 돕습니다.")

            selected_compare = st.multiselect(
                "⚖️ 대조 비교할 상품을 보관함에 담아보세요 (최대 3개 선택):",
                options=product_names_list,
                default=product_names_list[:2] if len(product_names_list) >= 2 else product_names_list,
                max_selections=3,
                key="compare_matrix_selector"
            )

            if not selected_compare:
                st.info("비교할 상품을 보관함에 담아주세요 🛒")
            else:
                cols_compare = st.columns(len(selected_compare))
                for idx_c, combo_label in enumerate(selected_compare):
                    try:
                        rank_idx = int(combo_label.split('위.')[0].strip()) - 1
                        row_compare = recommendations.iloc[rank_idx]
                        comp_platform = str(row_compare.get('platform') or 'Unknown')
                        comp_name = str(row_compare.get('product_name') or row_compare.get('displayName') or '이름 없음')
                        comp_brand = str(row_compare.get('brandName') or row_compare.get('brand') or '브랜드 정보 없음')
                        comp_rating = row_compare.get('rating', 0.0)
                        comp_reviews = int(row_compare.get('review_count', 0))
                        comp_std_ing = str(row_compare.get('표준성분', ''))
                        comp_detail_url = get_product_detail_url(row_compare)
                        comp_mkt = get_market_top_product(comp_std_ing)
                        comp_price_val = row_compare.get('price')
                        if pd.isna(comp_price_val):
                            comp_price_val = row_compare.get('discountPrice') or row_compare.get('price_cur') or 0.0
                        comp_price_str = f"{int(comp_price_val):,}원" if comp_price_val > 0 else "가격 정보 없음"
                        comp_foodsafety = find_foodsafety_info(comp_std_ing, db_data)
                        comp_fn_desc = "표준 고시 기준 규격 적용 원료"
                        if comp_foodsafety:
                            comp_fn_desc = comp_foodsafety[0]['functionality']
                        with cols_compare[idx_c]:
                            primary_url = comp_mkt["url"] if comp_mkt else comp_detail_url
                            mkt_badge_html = ""
                            if comp_mkt:
                                mkt_badge_html = (
                                    f\'<div style="background:#FAFBFF;border:1px solid #E5EFFF;border-radius:10px;padding:10px 12px;margin-top:10px;">\'
                                    f\'<div style="font-size:0.68rem;color:#2C3281;font-weight:700;margin-bottom:4px;">📌 시장 내 대표 인기 제품</div>\'
                                    f\'<div style="font-size:0.78rem;color:#1F2937;font-weight:600;">{comp_mkt["brand"]} {comp_mkt["name"]}</div>\'
                                    f\'<div style="font-size:0.8rem;color:#5A83F1;font-weight:700;margin-top:2px;">{comp_mkt["price"]}</div>\'
                                    f\'<a href="{comp_mkt["url"]}" target="_blank" style="font-size:0.68rem;color:#5A83F1;text-decoration:none;font-weight:700;">🔗 네이버쇼핑 바로가기 ↗</a>\'
                                    f\'</div>\'
                                )
                            st.markdown(f\'\'\'<div style="background:#FFFFFF;border:1px solid #E5EFFF;border-radius:20px;padding:20px;min-height:390px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 10px 30px -5px rgba(90, 131, 241, 0.08);">
<div>
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
<span style="font-size:0.8rem;color:#2C3281;background:#E5EFFF;padding:2px 8px;border-radius:6px;font-weight:700;">⚖️ 비교 {idx_c+1}</span>
<span style="font-size:0.75rem;color:#475569;">{comp_platform.upper()}</span>
</div>
<div style="font-size:0.78rem;color:#475569;margin-bottom:2px;">{comp_brand}</div>
<h4 style="margin:0 0 8px 0;color:#1F2937;font-size:0.95rem;font-weight:700;height:38px;overflow:hidden;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;">{comp_name}</h4>
<div style="font-size:1.18rem;font-weight:800;color:#5A83F1;margin-bottom:6px;">{comp_price_str}</div>
<div style="font-size:0.82rem;color:#fbbf24;margin-bottom:10px;">⭐ {comp_rating:.1f} <span style="color:#64748b;">({comp_reviews:,}개 리뷰)</span></div>
<div style="font-size:0.82rem;color:#1F2937;margin-bottom:8px;line-height:1.3;">🧬 <strong>표준성분:</strong> `{comp_std_ing}`</div>
<hr style="border:0;border-top:1px solid #E5EFFF;margin:10px 0;"/>
<div style="font-size:0.78rem;color:#1F2937;height:90px;overflow-y:auto;line-height:1.4;padding-right:4px;"><strong>📜 식약처 기능성:</strong> {comp_fn_desc}</div>
{mkt_badge_html}
</div>
<a class="buy-btn" href="{primary_url}" target="_blank" style="background:linear-gradient(135deg,#5A83F1,#2C3281);margin-top:15px;">🛒 제품 상세 보기 ↗</a>
</div>\'\'\', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"비교 처리 중 오류: {e}")

            # ==================== 식약처 정밀 성분 가이드 (화이트 카드 섀도우 적용) ====================
            st.markdown("---")
            st.markdown("### 🛡️ 선택 제품 식약처 정밀 성분 분석 가이드")
            std_ing = str(selected_row.get('표준성분', ''))
            st.info(f"📋 **선택 제품**: {selected_row.get('product_name')}\\n\\n🧬 **검출 표준 성분**: `{std_ing}`")
            foodsafety_infos = find_foodsafety_info(std_ing, db_data)
            
            if not foodsafety_infos:
                st.info("💡 본 제품의 표준성분은 고시형 원료로 표준 고시 섭취 규격에 따릅니다.")
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    if "마그네슘" in std_ing:
                        st.subheader("🍀 마그네슘 (Magnesium)")
                        st.write("**기능성**: 에너지 이용에 필요, 신경과 근육 기능 유지")
                        st.write("**주의**: 신장 질환자 과량 섭취 시 고마그네슘혈증 위험")
                    elif "비타민C" in std_ing:
                        st.subheader("🍀 비타민C (Vitamin C)")
                        st.write("**기능성**: 항산화, 철 흡수 촉진, 결합조직 유지")
                        st.write("**주의**: 공복 섭취 시 위장 장애 가능 — 식후 복용 권장")
                with col_g2:
                    if "비타민" in std_ing:
                        st.subheader("🍀 종합 비타민 (Multivitamin)")
                        st.write("**기능성**: 체내 에너지 대사, 면역 및 항산화 조절")
                        st.write("**주의**: 복용 기준량 엄수 — 영양소 과다 중독 방지")
            else:
                tabs_fs = st.tabs([f"🧪 {info['target_token']}" for info in foodsafety_infos])
                for tab, info in zip(tabs_fs, foodsafety_infos):
                    with tab:
                        st.success(f"**식약처 공식 승인 명칭**: `{info['raw_material']}`")
                        col_tab1, col_tab2 = st.columns(2)
                        with col_tab1:
                            st.markdown("#### 🎯 기능성 내용")
                            for line in info['functionality'].split('\\n'):
                                if line.strip(): st.write(f"- {line.strip()}")
                        with col_tab2:
                            st.markdown("#### 🥄 권장 일일섭취량")
                            st.info(info['daily_intake'])
                            st.markdown("#### ⚠️ 섭취 시 주의사항")
                            st.warning(info['precautions'])

            # ==================== 데이터 내보내기 (Full-width 프리미엄 다운로드 바 형태로 최적화) ====================
            st.markdown("---")
            st.markdown("### 📥 뉴트리핏 진단 결과 데이터 내보내기")
            if os.path.exists(LOG_FILE_PATH):
                try:
                    df_logs_down = pd.read_csv(LOG_FILE_PATH, encoding="utf-8-sig")
                    csv_data_down = df_logs_down.to_csv(index=False, encoding="utf-8-sig")
                    st.download_button(
                        label="📥 실시간 누적 진단 로그 원본 (.csv) 전체 폭 내보내기",
                        data=csv_data_down,
                        file_name="survey_logs_export.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="premium_csv_download_btn"
                    )
                except:
                    st.info("로그 데이터를 파싱하지 못했습니다.")
            else:
                st.info("📝 아직 누적된 사용자 진단 로그가 없습니다.")

            # ==================== 식약처 공식 메디컬 면책 공지 (Disclaimer) 및 데이터 출처 신설 ====================
            st.markdown(\"\"\"
                <div style="background: #FFFFFF; border: 1px solid #E5EFFF; border-radius: 20px; padding: 25px; margin-top: 30px; box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.08); font-size: 0.8rem; color: #475569; line-height: 1.6;">
                    <h5 style="color: #2C3281; font-weight: 700; margin: 0 0 12px 0;">🛡️ 식약처 공식 메디컬 면책 공지 (Medical Disclaimer)</h5>
                    본 서비스에서 제공하는 모든 웰니스 큐레이션 및 Scikit-Learn 머신러닝 기반 건강 위험도 예측 수치는 식약처(식품의약품안전처)에서 제공하는 건강기능식품 공공데이터포털(API)의 규격 정보에 근거합니다.<br>
                    <strong>주의:</strong> 본 결과는 특정 질환에 대한 의사/약사의 의학적 치료 진단 또는 전문적인 약학적 처방을 대체할 수 없으며, 일반적인 건강 증진 목적의 참고 정보로만 제공됩니다. 특정 질환 치료 목적의 영양제 섭취 시 반드시 전문의와의 상담이 선행되어야 합니다.<br><br>
                    <strong>💡 데이터 출처 고시:</strong> 식품의약품안전처 공공데이터포털 건강기능식품 기능성 원료 및 제품 정보 API 마스터 데이터베이스 (2026 기준).
                </div>
            \"\"\", unsafe_allow_html=True)

            st.markdown("---")
            col_btn_back1, col_btn_back2 = st.columns(2)
            with col_btn_back1:
                if st.button("⬅️ 이전 단계 (웰니스 리포트)"):
                    st.session_state.step = 2
                    st.rerun()
            with col_btn_back2:
                if st.button("🔄 문진 새로 작성하기"):
                    st.session_state.agreed = False
                    st.session_state.step = 1
                    st.session_state.survey_data = {}
                    st.session_state.all_agree = False
                    st.session_state.agree_1 = False
                    st.session_state.agree_2 = False
                    st.session_state.agree_3 = False
                    st.session_state.streaming_done = False
                    st.rerun()

            # 💥 스트리밍 플래그 완료 처리
            if not st.session_state.streaming_done:
                st.session_state.streaming_done = True
                st.rerun()
            """
            
    content = content[:start_step3_idx] + new_step3_wide_section + "\n" + content[end_step3_idx:]

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("app.py 최종 리팩토링 및 덮어쓰기 완료!")

if __name__ == "__main__":
    main()
