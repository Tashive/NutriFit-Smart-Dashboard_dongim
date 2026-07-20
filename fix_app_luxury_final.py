"""
app.py의 UI/UX 스타일 및 가독성을 최종 점검하고 완벽하게 개편하는 파이썬 스크립트입니다.
주요 수정 내역:
1. 모든 st.button 및 커스텀 버튼의 글자색을 어떤 모드에서도 화이트(#FFFFFF)로 강제 고정하여 토스 스타일 전체 동의 버튼의 텍스트가 파묻히는 문제를 근본적으로 해결.
2. 모든 입력 위젯(셀렉트박스, 멀티셀렉트, 텍스트 인풋 등)의 배경색을 순수 화이트(#FFFFFF)로 강제하고 라벨 및 입력 텍스트를 딥차콜(#1F2937)로 강제 지정하여 100% 가독성 확보.
3. 멀티셀렉트 선택 칩의 배경색을 소프트블루(#E5EFFF) 및 글자색을 딥블루(#2C3281)로 매핑.
4. 전역 슬레이트 블루 그라데이션 배경 및 글래스모피즘 카드 컴포넌트, 0.3s 이징 트랜지션을 완벽히 이식.
"""

def main():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. CSS 코드 전면 업데이트 (모든 버튼 글자색 화이트 강제 고정 스펙 포함)
    start_css_marker = '    st.markdown(\"\"\"\n        <style>\n        @import url(\'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap\');'
    end_css_marker = '        </style>\n    \"\"\", unsafe_allow_html=True)'
    
    start_css_idx = content.find(start_css_marker)
    end_css_idx = content.find(end_css_marker, start_css_idx)
    
    if start_css_idx == -1 or end_css_idx == -1:
        print("Error: CSS 마커를 찾지 못했습니다.")
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
            padding-top: 110px !important;
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
        
        /* ========== 모든 위젯 및 입력 폼 가독성 & 프리미엄 테이밍 (배경 화이트, 텍스트 딥차콜) ========== */
        input, select, textarea, [data-baseweb="select"], .stSelectbox div, .stMultiSelect div {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid rgba(90, 131, 241, 0.15) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease-in-out !important;
        }
        
        /* 멀티셀렉트 드롭다운 팝업 리스트 가독성 강제 고정 */
        div[role="listbox"] {
            background-color: #FFFFFF !important;
        }
        div[role="listbox"] li {
            color: #1F2937 !important;
            background-color: #FFFFFF !important;
        }
        div[role="listbox"] li:hover {
            background-color: #E5EFFF !important;
            color: #2C3281 !important;
        }
        
        /* 포커스 및 선택 시 브랜드 주색 (#5A83F1) 은은한 네온 효과 */
        input:focus, select:focus, textarea:focus {
            border-color: #5A83F1 !important;
            box-shadow: 0 0 10px rgba(90, 131, 241, 0.25) !important;
        }
        
        .stRadio label, .stCheckbox label, .stSelectbox label, .stMultiSelect label, .stSlider label, .stTextInput label, .stNumberInput label {
            color: #1F2937 !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p {
            color: #1F2937 !important;
        }
        
        /* 멀티셀렉트 선택된 태그 칩 (소프트블루 #E5EFFF 및 딥블루 #2C3281 매핑) */
        [data-baseweb="tag"] {
            background-color: #E5EFFF !important;
            color: #2C3281 !important;
            border: 1px solid rgba(90, 131, 241, 0.3) !important;
            border-radius: 8px !important;
        }
        [data-baseweb="tag"] span {
            color: #2C3281 !important;
        }
        
        /* ========== 스트림릿 기본 버튼 디자인 프리미엄 화이트/그라데이션 및 글자색 화이트 강제 고정 ========== */
        .stButton button {
            background: linear-gradient(135deg, #5A83F1, #2C3281) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 10px 24px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(90, 131, 241, 0.15) !important;
            transition: all 0.3s ease-in-out !important;
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(90, 131, 241, 0.3) !important;
            opacity: 0.95 !important;
        }
        .stButton button p, .stButton button span {
            color: #FFFFFF !important;
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
            height: 70px;
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
            background: rgba(255, 255, 255, 0.9) !important;
            backdrop-filter: blur(8px) !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            border-radius: 24px;
            padding: 22px;
            margin-bottom: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 590px;
            box-shadow: 0 20px 40px -15px rgba(0,0,0,0.05) !important;
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
            background: rgba(255, 255, 255, 0.9) !important;
            backdrop-filter: blur(8px) !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            border-radius: 24px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 20px 40px -15px rgba(0,0,0,0.05) !important;
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
    
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("전체 페이지 가독성 및 전체 동의 버튼 화이트 오버라이드 완료!")

if __name__ == "__main__":
    main()
