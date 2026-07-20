"""
app.py를 예술적인 D2C 브랜드사 플랫폼 수준으로 시각적 럭셔리 개편을 단행하는 스크립트입니다.
주요 변경 사항:
1. 전역 배경을 프리미엄 소프트 슬레이트 블루 그라데이션(#F8FAFC ~ #E2E8F0)으로 고정
2. 모든 카드와 대시보드 박스에 글래스모피즘(반투명 화이트 + 블러) 및 소프트 스모크 리얼 섀도우 적용
3. 모든 호버 모션에 0.3s 슬로우 ease-in-out 트랜지션 연동
4. 인풋, 셀렉트박스 등 위젯들의 컬러를 딥그레이(#374151) 및 프리미엄 블루 포커싱 네온 효과로 통일
5. GNB와 푸터 영역의 미니멀리즘 아키텍처 및 미학적 폰트 정돈
"""

def main():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. CSS 영역 전면 교체 (L399 ~ L636에 대응되는 st.markdown CSS 교체)
    start_css_marker = '    st.markdown(\"\"\"\n        <style>\n        @import url(\'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap\');'
    end_css_marker = '        </style>\n    \"\"\", unsafe_allow_html=True)'
    
    start_css_idx = content.find(start_css_marker)
    end_css_idx = content.find(end_css_marker, start_css_idx)
    
    if start_css_idx == -1 or end_css_idx == -1:
        print("Error: CSS 영역을 찾을 수 없습니다.")
        return

    new_luxury_css = """    st.markdown(\"\"\"
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap');

        /* ========== 전역 테마: 하이엔드 소프트 슬레이트 블루 그라데이션 고정 ========== */
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%) !important;
            color: #374151 !important;
        }
        
        /* 스트림릿 기본 탑 헤더 숨김 처리 */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        /* 메인 콘텐츠 영역 상단 헤드룸 및 와이드 여백 확보 */
        .main .block-container {
            padding-top: 130px !important;
            background: transparent !important;
        }

        /* 폰트 및 텍스트 컬러 지정 (정갈하고 정밀한 타이포그래피) */
        h1, h2, h3, h4, h5, h6, p, label, li {
            color: #1F2937 !important;
            font-family: 'Outfit', 'Noto Sans KR', sans-serif !important;
            letter-spacing: -0.3px !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(12px) !important;
            border-right: 1px solid rgba(90, 131, 241, 0.1) !important;
        }
        
        /* ========== 모든 위젯 및 입력 폼 가독성 & 프리미엄 테이밍 ========== */
        input, select, textarea, div[role="listbox"], [data-baseweb="select"], .stSelectbox, .stMultiSelect {
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: #374151 !important;
            border: 1px solid rgba(90, 131, 241, 0.15) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease-in-out !important;
        }
        
        /* 포커스 및 선택 시 브랜드 주색 (#5A83F1) 은은한 네온 효과 */
        input:focus, select:focus, textarea:focus {
            border-color: #5A83F1 !important;
            box-shadow: 0 0 10px rgba(90, 131, 241, 0.25) !important;
        }
        
        .stRadio label, .stCheckbox label, .stSelectbox label, .stMultiSelect label, .stSlider label, .stTextInput label, .stNumberInput label {
            color: #374151 !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
            color: #374151 !important;
        }
        
        [data-baseweb="tag"] {
            background-color: #E5EFFF !important;
            color: #2C3281 !important;
            border: 1px solid rgba(90, 131, 241, 0.3) !important;
            border-radius: 8px !important;
        }
        
        /* ========== 오버도즈 경고 펄스 애니메이션 ========== */
        @keyframes pulse-warning-anim {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.2); }
            70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        .pulse-warning {
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            background-color: rgba(255, 255, 255, 0.95) !important;
            animation: pulse-warning-anim 2s infinite;
        }
        
        /* ========== GNB 헤더 (반투명 화이트-인디고 엣지 스타일) ========== */
        .gnb-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.85);
            border-bottom: 1px solid rgba(90, 131, 241, 0.15);
            padding: 14px 48px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999999;
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 40px -10px rgba(44, 50, 129, 0.05);
            height: 75px;
            transition: all 0.3s ease-in-out;
        }
        .gnb-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.45rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2C3281, #5A83F1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .gnb-nav {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        .gnb-link {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: #475569 !important;
            padding: 8px 18px;
            border-radius: 10px;
            text-decoration: none;
            transition: all 0.3s ease-in-out;
            border: 1px solid transparent;
            cursor: pointer;
        }
        .gnb-link:hover {
            color: #2C3281 !important;
            background: rgba(90, 131, 241, 0.08);
            border-color: rgba(90, 131, 241, 0.1);
        }
        .gnb-link-highlight {
            color: #FFFFFF !important;
            background: #2C3281;
            box-shadow: 0 4px 15px rgba(44, 50, 129, 0.2);
        }
        .gnb-link-highlight:hover {
            background: #5A83F1;
            box-shadow: 0 6px 20px rgba(90, 131, 241, 0.3);
            color: #FFFFFF !important;
        }

        /* ========== 화이트 글래스모피즘 카드 및 스무스 이징 호버 ========== */
        .ecommerce-card {
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            border-radius: 24px;
            padding: 22px;
            margin-bottom: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 590px;
            box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.04) !important;
            transition: all 0.3s ease-in-out !important;
        }
        .ecommerce-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 30px 60px -15px rgba(90, 131, 241, 0.18) !important;
            border-color: rgba(90, 131, 241, 0.4) !important;
        }
        .card-badge {
            font-size: 0.7rem;
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 700;
            margin-right: 4px;
            display: inline-block;
            transition: all 0.3s ease-in-out;
        }
        .card-badge:hover { opacity: 0.8; transform: scale(1.04); }
        .badge-goal { background: #E5EFFF; color: #2C3281; }
        .badge-platform { background: rgba(90, 131, 241, 0.1); color: #5A83F1; }
        .badge-form { background: rgba(255, 255, 255, 0.6); color: #475569; border: 1px solid rgba(255, 255, 255, 0.8); }
        .buy-btn {
            display: block;
            width: 100%;
            text-align: center;
            background: linear-gradient(135deg, #5A83F1, #2C3281);
            color: white !important;
            padding: 11px 0;
            border-radius: 12px;
            font-weight: 700;
            text-decoration: none;
            font-size: 0.88rem;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(90, 131, 241, 0.15);
            transition: all 0.3s ease-in-out;
        }
        .buy-btn:hover {
            opacity: 0.95;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(90, 131, 241, 0.3);
        }

        /* ========== 유틸리티 사이드카드 (글래스모피즘 & 0.3s 모션) ========== */
        .side-util-card {
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            border-radius: 24px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.04) !important;
            transition: all 0.3s ease-in-out !important;
        }
        .side-util-card:hover {
            box-shadow: 0 30px 60px -15px rgba(90, 131, 241, 0.12) !important;
            border-color: rgba(90, 131, 241, 0.3) !important;
        }
        .side-section-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #2C3281;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        /* ========== 아웃링크 트리플 버튼 덱 ========== */
        .outlink-deck {
            display: flex;
            gap: 8px;
            margin-top: 10px;
        }
        .outlink-btn {
            flex: 1;
            text-align: center;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 8px 6px;
            border-radius: 10px;
            text-decoration: none;
            transition: all 0.3s ease-in-out;
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

        /* ========== 미니멀 엔터프라이즈 푸터 ========== */
        .enterprise-footer {
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(10px) !important;
            border-top: 1px solid rgba(90, 131, 241, 0.15) !important;
            border-radius: 24px 24px 0 0;
            padding: 36px 48px;
            margin-top: 48px;
            text-align: center;
            box-shadow: 0 -10px 40px -10px rgba(90, 131, 241, 0.04) !important;
        }
        .footer-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.20rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2C3281, #5A83F1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .footer-text {
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 0.78rem;
            color: #64748b;
            line-height: 1.7;
        }
        .footer-divider {
            border: 0;
            border-top: 1px solid rgba(90, 131, 241, 0.1);
            margin: 16px 0;
        }
        </style>
    \"\"\", unsafe_allow_html=True)"""
    
    content = content[:start_css_idx] + new_luxury_css + content[end_css_idx + len(end_css_marker):]

    # 2. 4열 추천 제품 카드의 디자인 럭셔리 튜닝 (render_product_grid 함수 내 card_style 수정)
    # 선택된 카드 스타일과 이미지 백그라운드 색상을 은은한 파스텔 글래스로 리뉴얼합니다.
    content = content.replace(
        'card_style = "border: 2px solid #5A83F1; background: #E5EFFF; box-shadow: 0 10px 25px rgba(90, 131, 241, 0.15);" if is_selected else ""',
        'card_style = "border: 1.5px solid #2C3281; background: rgba(90, 131, 241, 0.06); box-shadow: 0 15px 35px rgba(44, 50, 129, 0.1);" if is_selected else ""'
    )
    
    content = content.replace(
        'background: #FAFBFF; display: flex; justify-content: center; align-items: center;',
        'background: rgba(255, 255, 255, 0.7); display: flex; justify-content: center; align-items: center;'
    )
    
    # 3. 토스 스타일 동의 컨테이너를 글래스모피즘 화이트로 마운트
    content = content.replace(
        'background: #FFFFFF; border: 1px solid #E5EFFF; border-radius: 20px; padding: 25px; box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.08);',
        'background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 24px; padding: 25px; box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.04);'
    )

    # 4. Step 2 결과 웰니스 스코어 카드 글래스모피즘 입히기 (L1192 부근)
    # 원래: background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 10px;
    # 변경: background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 20px; box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.04);
    content = content.replace(
        'background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 10px;',
        'background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 20px; box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.04);'
    )
    
    # 텍스트 컬러 지정 교체 (Step 2 스코어 보너스 텍스트)
    content = content.replace(
        '<h4 style="margin: 2px 0 6px 0; color: #f8fafc;">{key}</h4>',
        '<h4 style="margin: 2px 0 6px 0; color: #1F2937;">{key}</h4>'
    )
    content = content.replace(
        '<span style="font-size: 0.85rem; color: #94a3b8;">영양소 성분</span>',
        '<span style="font-size: 0.85rem; color: #64748b;">영양소 성분</span>'
    )
    content = content.replace(
        '<span style="font-size: 1.8rem; font-weight: 800; color: #10b981;">+{score:.2f}</span>',
        '<span style="font-size: 1.8rem; font-weight: 800; color: #5A83F1;">+{score:.2f}</span>'
    )
    content = content.replace(
        '<span style="font-size: 0.8rem; color: #a7f3d0; background: rgba(16, 185, 129, 0.1); padding: 2px 6px; border-radius: 5px;">{comment}</span>',
        '<span style="font-size: 0.8rem; color: #2C3281; background: #E5EFFF; padding: 2px 6px; border-radius: 5px;">{comment}</span>'
    )

    # 5. Step 2 우측 AI 패턴 분석 카드도 럭셔리 매핑 (L1212 부근)
    # background: linear-gradient(135deg, #1e1b4b, #311042); border: 1px solid rgba(167, 139, 250, 0.3);
    content = content.replace(
        'background: linear-gradient(135deg, #1e1b4b, #311042); border: 1px solid rgba(167, 139, 250, 0.3); border-radius: 12px; padding: 20px; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);',
        'background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 20px; padding: 20px; box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.04);'
    )
    content = content.replace(
        '<h4 style="margin: 0 0 10px 0; color: #c084fc; font-family: \'Outfit\', \'Noto Sans KR\', sans-serif;">🤖 AI 건강 패턴 분석 (ML 가동 대기)</h4>',
        '<h4 style="margin: 0 0 10px 0; color: #2C3281; font-family: \'Outfit\', \'Noto Sans KR\', sans-serif;">🤖 AI 건강 패턴 분석 (ML 가동 대기)</h4>'
    )
    content = content.replace(
        '<p style="font-size: 0.9rem; color: #e9d5ff; margin-bottom: 15px; line-height: 1.4;">',
        '<p style="font-size: 0.9rem; color: #475569; margin-bottom: 15px; line-height: 1.4;">'
    )
    content = content.replace(
        '<div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 8px;">',
        '<div style="display: flex; justify-content: space-between; align-items: center; background: #FAFBFF; border: 1px solid #E5EFFF; padding: 8px 12px; border-radius: 8px;">'
    )
    content = content.replace(
        '<span style="font-size: 0.8rem; color: #a78bfa;">📊 문진 데이터 축적 상태</span>',
        '<span style="font-size: 0.8rem; color: #2C3281; font-weight:600;">📊 문진 데이터 축적 상태</span>'
    )
    content = content.replace(
        '<span style="background: rgba(167, 139, 250, 0.2); color: #f472b6; font-weight: 700; padding: 2px 10px; border-radius: 20px; font-size: 0.85rem;">',
        '<span style="background: #E5EFFF; color: #5A83F1; font-weight: 700; padding: 2px 10px; border-radius: 20px; font-size: 0.85rem;">'
    )
    content = content.replace(
        '<div style="margin-top: 15px; border-top: 1px dashed rgba(167, 139, 250, 0.2); padding-top: 10px; font-size: 0.75rem; color: #a78bfa; text-align: center;">',
        '<div style="margin-top: 15px; border-top: 1px dashed #E5EFFF; padding-top: 10px; font-size: 0.75rem; color: #475569; text-align: center;">'
    )

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("D2C 웰니스 브랜드 스타일 가이드 개편 완료!")

if __name__ == "__main__":
    main()
