"""
app.py의 UI/UX 완성도를 스타일 가이드에 맞춰 최종 개편하는 파이썬 스크립트입니다.
주요 변경 사항:
1. 전역 테마 독립형 프리미엄 컬러칩 적용 (전역 배경을 소프트 그레이시 블루 #F4F7FF로 지정, 카드 내벽을 화이트 #FFFFFF로 처리)
2. GNB 고정 겹침 현상 해결 (기본 stHeader 감추기, position: fixed로 GNB 고정 및 콘텐츠 padding-top: 110px 강제 적용)
3. 아이콘 깨짐 현상 박멸 (span, div, button 등의 font-family 전역 !important 지정 해제 및 예외 처리)
4. 모든 화이트 카드 컴포넌트에 은은한 블루 그림자 및 곡률 추가
"""

def main():
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = '    st.markdown("""\n        <style>\n        @import url(\'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;700&display=swap\');'
    end_marker = '        </style>\n    """, unsafe_allow_html=True)'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: CSS 영역 시작/끝 마커를 찾지 못했습니다.")
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
    
    # 덮어쓰기 영역 지정 치환
    content = content[:start_idx] + new_css + content[end_idx + len(end_marker):]
    
    # 2. 분석 대상자 프로필 배너 배경 수정
    profile_target = 'background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px;'
    profile_replace = 'background: #FFFFFF; border: 1px solid #E5EFFF; border-radius: 20px; box-shadow: 0 10px 30px -5px rgba(90, 131, 241, 0.08);'
    
    content = content.replace(profile_target, profile_replace)

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("app.py 프리미엄 컬러칩 및 레이아웃 패치 적용 성공!")

if __name__ == "__main__":
    main()
